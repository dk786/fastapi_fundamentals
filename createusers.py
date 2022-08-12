from sqlmodel import Session, create_engine,select

import db
from schemas import User


def read_credentials_from_file(filename):
    engine = db.engine
    session = Session(engine)
    with open(filename) as users:
        for usr in users:
            username, password = usr.split(",")
            create_user(password, session, username)
            get_data(session, username)


def create_user(password, session, username):
    new_user = User(username=username.strip())
    new_user.set_password(password.strip())
    session.add(new_user)
    session.commit()


def get_data(session, username):
    usrs = session.exec(select(User).where(User.username == username))
    for usr in usrs:
        print(f'user: {usr}')



if __name__ == "__main__":
    read_credentials_from_file("users.txt")
