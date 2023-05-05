from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    token: str


@dataclass
class CryptoKey:
    key: bytes


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    crypto: CryptoKey


def load_config(path: str) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  db=DatabaseConfig(database=env('POSTGRES_DB'),
                                    db_host=env('POSTGRES_HOST'),
                                    db_user=env('POSTGRES_USER'),
                                    db_password=env('POSTGRES_PASSWORD')),
                  crypto=CryptoKey(key=env('CRYPTO_KEY').encode('utf-8')))
