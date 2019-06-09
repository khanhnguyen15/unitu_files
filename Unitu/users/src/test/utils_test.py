from flask_bcrypt import Bcrypt
import jwt
import datetime

bcrypt = Bcrypt()

class DatabaseRow:
    def __init__(self, id, username, email, firstName, lastName, password, expire_seconds):
        self.id = id
        self.username = username
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.isActive = False
        self.password = bcrypt.generate_password_hash(password).decode()
        self.expired_seconds = expire_seconds

    def convert_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "isActive": self.isActive
        }

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    seconds=self.expired_seconds
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                "my_precious",
                algorithm='HS256'
            )
        except Exception as e:
            return e

all_rows = [
    DatabaseRow(1, "phu555", "phu555@mail.com", "Phu1", "Sakulwongtana1", "password1", 30),
    DatabaseRow(2, "phu556", "phu556@mail.com", "Phu2", "Sakulwongtana2", "password2", 30),
    DatabaseRow(3, "phu557", "phu557@mail.com", "Phu3", "Sakulwongtana3", "password3", 30),
]

def reset_all_rows():
    global all_rows

    for r in all_rows:
        r.isActive = False
        r.expired_seconds = 30


def user_query_all():
    return all_rows

def filter_by(username=None, email=None, id=None):
    for r in all_rows:
        if r.username == username:
            return FirstWrapper(r)

        if r.email == email:
            return FirstWrapper(r)

        if r.id == id:
            return FirstWrapper(r)

    return FirstWrapper(None)

def filter(or_statement):
    user_id_1 = or_statement.clauses[0].right.value
    user_id_2 = or_statement.clauses[1].right.value

    out_1 = filter_by(username=user_id_1)
    if out_1.first() is not None:
        return out_1

    out_2 = filter_by(email=user_id_2)
    if out_2.first() is not None:
        return out_2

    out_1 = filter_by(email=user_id_1)
    if out_1.first() is not None:
        return out_1

    out_2 = filter_by(username=user_id_2)
    if out_2.first() is not None:
        return out_2

    return FirstWrapper(None)

class FirstWrapper:
    def __init__(self, return_user):
        self.return_user = return_user

    def first(self):
        return self.return_user
