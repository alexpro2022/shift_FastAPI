from fastapi_users import InvalidPasswordException

from app.config.app_config import app_conf


def password_length_validator(password: str) -> None:
    if len(password) < app_conf.password_length:
        raise InvalidPasswordException(
            f"Пароль должен быть длиной не менее {app_conf.password_length} символов."
        )


def password_content_validator(password: str, email: str) -> None:
    if email in password:
        raise InvalidPasswordException("В пароле не должно содержаться e-mail.")
