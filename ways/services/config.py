from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    local_database_path: str = r'data/Way.db'
    local_table_name: str = 'New'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)