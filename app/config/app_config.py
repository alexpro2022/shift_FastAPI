from app.config._base import BaseConf, EmailStr, SecretStr


class Settings(BaseConf):
    URL_PREFIX: str = "/api/v1/"
    DEFAULT_STR: str = "To be implemented in .env file"
    ADMIN_ONLY: str = "__Только для админов/суперюзеров:__ "
    AUTH_ONLY: str = "__Только для авторизованных пользователей:__ "
    ALL_USERS: str = "__Для всех пользователей:__ "

    app_title: str = f"App title {DEFAULT_STR}"
    app_description: str = f"App description {DEFAULT_STR}"
    salary_precision: int = 8
    salary_scale: int = 2

    # authentication
    secret_key: SecretStr = f"Secret key {DEFAULT_STR}"
    admin_email: EmailStr = "adm@adm.com"
    admin_password: str = "admpw"
    password_length: int = 3
    token_lifetime: int = 3600
    token_url: str = "auth/jwt/login"
    auth_backend_name: str = "jwt"


app_conf = Settings()
