Messanger
====

This is Messanger Api realised by FastApi.

<< Installing >>

python -m setup.py install


<< Docs >>

GET  /index
----
Request:
  No parameters
  
POST  /login
----
Request:
  {
  "user_form": {
    "login": "string",
    "password": "string"
  }
}
GET  /login

Request:
token *
string

POST  /user
----
Request:
{
  "user": {
    "email": "string",
    "login": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
  }
}

GET  /user/contact
----
Request:
token *
string
(query)


POST  /user/contact
----
Request:
{
  "contact": {
    "token": "string",
    "friend_login": "string"
  }
}

GET  /user/contact/message
----
Request:
token *
string
(query); 
contact_id *
string

POST  /user/contact/message
----
Request:

{
  "message": {
    "token": "string",
    "contact_id": 0,
    "message": "string"
  }
}
