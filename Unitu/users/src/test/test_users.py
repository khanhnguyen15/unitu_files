import json
from src.test.base import BaseTestCase
from src.test.utils_test import user_query_all, filter_by, \
        all_rows, filter, DatabaseRow

import mock
from unittest.mock import MagicMock
from parameterized import parameterized

from src.api.models import User
import time

class TestUsers(BaseTestCase):
    def test_ping(self):
        with self.client:
            response = self.client.get(
                '/users/ping'
            )
            self.assertTrue(response.status_code == 200)

            data = json.loads(response.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'pong! users')

    def test_get_all_users(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.all = user_query_all
                response = self.client.get(
                    '/users'
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "success")
                self.assertTrue(len(data["data"]["users"]) == 3)

                self.assertTrue(data["data"]["users"][0] == user_query_all()[0].convert_json())
                self.assertTrue(data["data"]["users"][1] == user_query_all()[1].convert_json())
                self.assertTrue(data["data"]["users"][2] == user_query_all()[2].convert_json())

    def test_users_login_no_post_data(self):
        with self.client:
            response = self.client.post(
                '/users/login'
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid Payload")

    def test_user_login_empty_post_data(self):
        with self.client:
            response = self.client.post(
                '/users/login',
                json={}
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid Payload")


    def test_users_login_no_username_or_email(self):
        with self.client:
            response = self.client.post(
                '/users/login',
                json={"password": "password1"}
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Username or Email isn't found")

    def test_users_login_no_password(self):
        with self.client:
            response = self.client.post(
                '/users/login',
                json={"user_identification": "phu555"}
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Password isn't found")

    def test_users_login_not_in_database(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by
                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu55", "password": "password1"}
                )

                self.assertTrue(response.status_code == 404)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Username or Email with Password doesn't not matched")

    def test_users_login_password_not_correct(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by
                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555", "password": "password123r4t45y6urgdf"}
                )

                self.assertTrue(response.status_code == 404)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Username or Email with Password doesn't not matched")

    def test_users_login_success_loging_from_username(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query, mock.patch('src.db.session') as session:
                user_query.filter_by = filter_by

                commit_mock = MagicMock()
                session.commit = commit_mock

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555", "password": "password1"}
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully Log in")
                self.assertTrue(data["token"] is not None)
                self.assertTrue(all_rows[0].isActive)
                self.assertTrue(commit_mock.called)

    def test_users_login_success_loging_from_email(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query, mock.patch('src.db.session') as session:
                user_query.filter_by = filter_by

                commit_mock = MagicMock()
                session.commit = commit_mock

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555@mail.com", "password": "password1"}
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully Log in")
                self.assertTrue(data["token"] is not None)
                self.assertTrue(all_rows[0].isActive)
                self.assertTrue(commit_mock.called)

    def test_users_loging_internal_error(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query, mock.patch('src.db.session') as session:
                user_query.filter_by = filter_by

                def raise_error():
                    raise ValueError()

                session.commit = raise_error

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555@mail.com", "password": "password1"}
                )

                self.assertTrue(response.status_code == 500)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Internal Error")
                self.assertTrue(data.get("token") is None)

    def test_users_add_no_payload(self):
        with self.client:
            response = self.client.post(
                '/users/add',
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid Payload")

    def test_users_add_empty_payload(self):
        with self.client:
            response = self.client.post(
                '/users/add',
                json={}
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid Payload")

    @parameterized.expand([
        ["a", None, "b", "c", "d"],
        ["a", "e", None, None, "d"],
        [None, "e", None, None, "d"],
        [None, None, None, None, "d"],
    ])
    def test_users_add_not_filled_json(self, firstName, lastName, email, username, password):
        with self.client:
            response = self.client.post(
                '/users/add',
                json={
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email,
                    "username": username,
                    "password": password
                }
            )

            self.assertTrue(response.status_code == 400)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Not Enough Information to create account")

    def test_user_add_already_exists_email(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter = filter
                response = self.client.post(
                    '/users/add',
                    json={
                        "firstName": "Phu1",
                        "lastName": "Sakulwongtana1",
                        "email": "phu555@mail.com",
                        "username": "phu654",
                        "password": "password1"
                    }
                )

                self.assertTrue(response.status_code == 400)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Username or Email Already Exists.")

    def test_user_add_already_exists_username(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter = filter
                response = self.client.post(
                    '/users/add',
                    json={
                        "firstName": "Phu1",
                        "lastName": "Sakulwongtana1",
                        "email": "phu555dsafsd@mail.com",
                        "username": "phu555",
                        "password": "password1"
                    }
                )

                self.assertTrue(response.status_code == 400)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Username or Email Already Exists.")

    def test_user_add_already_exists_both(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter = filter
                response = self.client.post(
                    '/users/add',
                    json={
                        "firstName": "Phu1",
                        "lastName": "Sakulwongtana1",
                        "email": "phu555@mail.com",
                        "username": "phu555",
                        "password": "password1"
                    }
                )

                self.assertTrue(response.status_code == 400)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Username or Email Already Exists.")

    def test_user_add_success(self):
        with self.client:
            with mock.patch('src.db.session') as session, mock.patch('src.api.models.User.query') as user_query:
                user_query.filter = filter

                session_commit = MagicMock()
                session.commit = session_commit

                session_add = MagicMock()
                session.add = session_add

                response = self.client.post(
                    '/users/add',
                    json={
                        "firstName": "Phu1",
                        "lastName": "Sakulwongtana1",
                        "email": "phu558@mail.com",
                        "username": "phu559",
                        "password": "password1"
                    }
                )

                self.assertTrue(response.status_code == 201)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "User successfully added")

                # It is difficult to patch User
                self.assertTrue(session_add.call_args_list[0][0][0].username == "phu559")
                self.assertTrue(session_add.call_args_list[0][0][0].email == "phu558@mail.com")
                self.assertTrue(session_add.call_args_list[0][0][0].firstName == "Phu1")
                self.assertTrue(session_add.call_args_list[0][0][0].lastName == "Sakulwongtana1")
                session_commit.assert_called_once()

    def test_users_status_no_header(self):
        # user_token = all_rows[0].encode_auth_token()

        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by

                response = self.client.get(
                    '/users/status'
                )

                self.assertTrue(response.status_code == 403)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Invalid Token")

    def test_users_status_no_one_token(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by

                response = self.client.get(
                    '/users/status',
                    headers={"Authorization": "test"}
                )

                self.assertTrue(response.status_code == 403)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Authorization Token not Found")

    def test_users_status_invaid_token(self):
        user_token = "hi this is very wrong token"

        with self.client:
            response = self.client.get(
                '/users/status',
                headers={"Authorization" : f"Bearer {user_token}"}
            )
            self.assertTrue(response.status_code == 401)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid token.")

    def test_users_status_expired_token(self):
        all_rows[0].expired_seconds = -10
        user_token = all_rows[0].encode_auth_token()

        with self.client:
            response = self.client.get(
                '/users/status',
                headers={"Authorization" : f"Bearer {user_token.decode()}"}
            )
            self.assertTrue(response.status_code == 401)
            data = json.loads(response.data.decode())

            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Signature expired.")

    def test_users_status_token_id_not_found(self):
        not_in_db_user = DatabaseRow(
            4, "phu558", "phu558@mail.com", "Phu4", "Sakulwongtana4", "password4", 30
        )

        user_token = not_in_db_user.encode_auth_token()
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by

                response = self.client.get(
                    '/users/status',
                    headers={"Authorization" : f"Bearer {user_token.decode()}"}
                )

                self.assertTrue(response.status_code == 401)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Invalid User either not active or not exists")

    def test_users_status_token_id_not_active(self):
        user_token = all_rows[0].encode_auth_token()

        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by

                response = self.client.get(
                    '/users/status',
                    headers={"Authorization" : f"Bearer {user_token.decode()}"}
                )

                self.assertTrue(response.status_code == 401)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Invalid User either not active or not exists")

    def test_users_status_success(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.filter_by = filter_by

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555@mail.com", "password": "password1"}
                )

                data = json.loads(response.data.decode())
                user_token = data['token']

                response = self.client.get(
                    '/users/status',
                    headers={"Authorization" : f"Bearer {user_token}"}
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully fetch user data.")
                self.assertTrue(data["data"] == all_rows[0].convert_json())

    def test_users_logout_success_from_email(self):
        """Since we have tested the authenticate decorate in status, we don't need another one
        there will be user avaliable because the authenticate"""

        with self.client:
            with mock.patch('src.api.models.User.query') as user_query, mock.patch('src.db.session') as session:
                user_query.filter_by = filter_by

                session.commit = MagicMock()

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555@mail.com", "password": "password1"}
                )

                data = json.loads(response.data.decode())
                user_token = data['token']

                response = self.client.post(
                    '/users/logout',
                    headers={"Authorization" : f"Bearer {user_token}"}
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                session.commit.assert_called()

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully Logout")
                self.assertFalse(all_rows[0].isActive)

    def test_users_logout_success_from_user(self):
        """Since we have tested the authenticate decorate in status, we don't need another one
        there will be user avaliable because the authenticate"""

        with self.client:
            with mock.patch('src.api.models.User.query') as user_query, mock.patch('src.db.session') as session:
                user_query.filter_by = filter_by

                session.commit = MagicMock()

                response = self.client.post(
                    '/users/login',
                    json={"user_identification": "phu555", "password": "password1"}
                )

                data = json.loads(response.data.decode())
                user_token = data['token']

                response = self.client.post(
                    '/users/logout',
                    headers={"Authorization" : f"Bearer {user_token}"}
                )

                self.assertTrue(response.status_code == 200)
                data = json.loads(response.data.decode())

                session.commit.assert_called()

                self.assertTrue(data["status"] == "success")
                self.assertTrue(data["message"] == "Successfully Logout")
                self.assertFalse(all_rows[0].isActive)

    def test_get_all_users_internal_error(self):
        with self.client:
            with mock.patch('src.api.models.User.query') as user_query:
                user_query.all = self.stupidSideEffect
                response = self.client.get(
                    '/users'
                )

                self.assertTrue(response.status_code == 500)
                data = json.loads(response.data.decode())

                self.assertTrue(data["status"] == "fail")
                self.assertTrue(data["message"] == "Internal Error")
                self.assertTrue(data["error_message"] == "error message test")
