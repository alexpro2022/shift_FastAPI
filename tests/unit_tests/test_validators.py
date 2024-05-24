import pytest
from fastapi_users import InvalidPasswordException

from app.config.app_config import app_conf
from app.user.validators import password_content_validator, password_length_validator

EMAIL = "email@email.com"
VALID_CONTENT_ARGS = ("password", EMAIL)
INVALID_CONTENT_ARGS = (f"password{EMAIL}", EMAIL)
INVALID_CONTENT_MSG = "В пароле не должно содержаться e-mail."

VALID_LENGTH_ARGS = ("a" * (app_conf.password_length),)
INVALID_LENGTH_ARGS = ("a" * (app_conf.password_length - 1),)
INVALID_LENGTH_MSG = (
    f"Пароль должен быть длиной не менее {app_conf.password_length} символов."
)


@pytest.mark.parametrize(
    "method, valid_args, invalid_args, error_msg",
    (
        (
            password_content_validator,
            VALID_CONTENT_ARGS,
            INVALID_CONTENT_ARGS,
            INVALID_CONTENT_MSG,
        ),
        (
            password_length_validator,
            VALID_LENGTH_ARGS,
            INVALID_LENGTH_ARGS,
            INVALID_LENGTH_MSG,
        ),
    ),
)
def test_password_validators(method, valid_args, invalid_args, error_msg) -> None:
    method(*valid_args)
    with pytest.raises(InvalidPasswordException, match=error_msg):
        method(*invalid_args)
