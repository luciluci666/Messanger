from fastapi import APIRouter, Body, Depends, HTTPException
import uuid
from starlette import status
from sqlalchemy import or_

from .forms import UserLoginForm, UserCreateForm, CreateContact, CreateMessage
from .models import AuthToken, connect_db, User, Contact, Message
from .utils import get_password_hash
from .auth import check_auth_token


router = APIRouter()

@router.get('/')
def index():
    return HTTPException(status_code=status.HTTP_200_OK)

@router.post('/login', name='user:login')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.login).one_or_none()
    if not user:
        user = database.query(User).filter(User.login == user_form.login).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error' : 'Email/login/passwword invalid'}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()

    return {'auth_token' : auth_token.token}

@router.post('/user', name='user:create')
def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(or_(User.email == user.email, User.login == user.login)).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email/login already exist')

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        login=user.login,
        first_name=user.first_name,
        last_name=user.last_name
    )
    database.add(new_user)
    database.commit()
    
    return {'user_id' : new_user.id}


@router.get('/user', name='user:get')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()

    return  {'id' : user.id, 'email' : user.email, 'login' : user.login}


@router.post('/user/contact', name='contact:create')
def create_contact(contact: CreateContact = Body(..., embed=True), database=Depends(connect_db)):
    try:
        user = database.query(AuthToken).filter(AuthToken.token == contact.token).one_or_none().user_id
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not validated')

    try:
        friend = database.query(User).filter(User.login == contact.friend_login).one_or_none().id
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This login is undefined')

    exists_contact = database.query(Contact).filter(Contact.first_id == user, Contact.second_id == friend).one_or_none()
    exists_contact_1 = database.query(Contact).filter(Contact.first_id == friend, Contact.second_id == user).one_or_none()
    if exists_contact or exists_contact_1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This contact already exist')

    new_contact = Contact(
        first_id = user,
        second_id = friend
    )

    database.add(new_contact)
    database.commit()

    return {'friend_id' : friend}


@router.get('/user/contact', name='contact:get')
def get_contact(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    contacts = database.query(Contact).filter(or_(Contact.first_id == user.id, Contact.second_id == user.id)).all()

    contacts_list = []
    for contact in contacts:
        if contact.first_id == user.id:
            friend_id = contact.second_id
        else:
            friend_id = contact.first_id
        friend_login = database.query(User).filter(User.id == friend_id).one_or_none().login
        contacts_list.append({
            'contact_id' : contact.id,
            'friend_id' : friend_id,
            'friend_login' : friend_login,
        })

    return  {'contacts' : contacts_list}

@router.post('/user/contact/message', name='message:create')
def create_message(message: CreateMessage = Body(..., embed=True), database=Depends(connect_db)):
    try:
        user_id = database.query(AuthToken).filter(AuthToken.token == message.token).one_or_none().user_id
        user = database.query(User).filter(User.id == user_id).one_or_none()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not validated')
    contact = database.query(Contact).filter(Contact.id == message.contact_id, or_(Contact.first_id == user.id, Contact.second_id == user.id)).one_or_none()
    if not contact:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This chat is not avaible')
    
    new_message = Message(
        contact_id = contact.id,
        send_id = user.id,
        msg = message.message
    )
    database.add(new_message)
    database.commit()

    return {'message' : '200'}


@router.get('/user/contact/message', name='message:get')
def get_user(contact_id: str, token: AuthToken = Depends(check_auth_token),  database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()

    contact = database.query(Contact).filter(Contact.id == contact_id, or_(Contact.first_id == user.id, Contact.second_id == user.id)).one_or_none()
    if not contact:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This chat is not avaible')

    messages = database.query(Message).filter(Message.contact_id == contact.id).all()
    message_list = []
    for message in messages:
        message_list.append({
            'sender' : message.send_id,
            'msg' : message.msg,
            'status' : message.status,
            'created_at' : message.created_at
        })


    return  {'messages' : message_list}
