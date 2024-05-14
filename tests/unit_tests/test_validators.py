import pytest
from config.app_config import app_conf
from fastapi_users import InvalidPasswordException

from app.user.validators import password_content_validator, password_length_validator
from tests.utils import check_exception_info

INVALID_CONTENT_MSG = "В пароле не должно содержаться e-mail."
INVALID_CONTENT_ARGS = ("email-password", "email")
VALID_CONTENT_ARGS = ("password", "email")

INVALID_LENGTH_MSG = (
    f"Пароль должен быть длиной не менее {app_conf.password_length} символов."
)
INVALID_LENGTH_ARGS = ("a" * (app_conf.password_length - 1),)
VALID_LENGTH_ARGS = ("a" * (app_conf.password_length),)


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
    with pytest.raises(InvalidPasswordException) as exc_info:
        method(*invalid_args)
    check_exception_info(exc_info, error_msg)
