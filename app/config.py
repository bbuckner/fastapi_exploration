from pydantic import BaseSettings


class Settings(BaseSettings):
    # pydantic will take all environment variables and convert to lowercase.
    # will perform type checking on already existing variables.
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
