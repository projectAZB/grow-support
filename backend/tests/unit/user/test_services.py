import pytest
from werkzeug.security import check_password_hash

from backend.user.contracts import UserRequest
from backend.user.errors import UserError
from backend.user.models import UserModel
from backend.user.services import create_user_service, login_user_service

test_username = 'test_username'
test_password = 'pw123'


def _create_existing_user(database, username, password) -> UserModel:
    existing_user = UserModel(username=username)
    existing_user.set_password(password)
    database.session.add(existing_user)
    database.session.commit()
    return existing_user


@pytest.mark.parametrize('user_exists_already', [False, True])
def test_create_user_service(database, user_exists_already):
    if user_exists_already:
        _create_existing_user(database, test_username, test_password)

    request = UserRequest(username=test_username, password=test_password)
    response = create_user_service(database, request)
    assert response.success == (not user_exists_already)
    if user_exists_already:
        assert response.errors[0] == UserError.ACCOUNT_ALREADY_EXISTS.value.format(username=test_username)
    else:
        user_model: UserModel = database.session.query(UserModel).filter_by(username=request.username).one()
        assert user_model.username == request.username
        assert check_password_hash(user_model.password, test_password)


@pytest.mark.parametrize('user_exists, password_correct', [(False, False), (True, True), (True, False)])
def test_login_user_service(database, user_exists, password_correct):
    if user_exists:
        _create_existing_user(database, test_username, test_password)

    request = UserRequest(username=test_username, password=test_password if password_correct else 'nottherightpw')
    response = login_user_service(database, request)
    if user_exists and password_correct:
        assert response.success
    elif user_exists and not password_correct:
        assert not response.success
    elif not user_exists:
        assert not response.success
