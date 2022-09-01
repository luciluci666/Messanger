from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL

def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table users(
        id integer not null primary key,
        email varchar(256),
        login varchar(256),
        password varchar(256),
        first_name varchar(256),
        last_name varchar(256),
        created_at varchar(256)
    );
    """)

    session.execute("""create table auth_token(
        id integer not null primary key,
        token varchar(256),
        user_id integer references users,
        created_at varchar(256)
    );
    """)

    session.execute("""create table contact(
        id integer not null primary key,
        first_id integer references users,
        second_id integer references users,
        created_at varchar(256)
    );
    """)

    session.execute("""create table message(
        id integer not null primary key,
        contact_id integer references contact,
        send_id integer references users,
        msg text,
        status varchar(256),
        created_at varchar(256)
    );
    """)

    session.close()

if __name__ == '__main__':
    main()