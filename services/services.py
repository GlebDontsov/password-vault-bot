from cryptography.fernet import Fernet
from aiogram.types import Message
import asyncio

from bot import config


async def delete_message(message: Message, delay: int):
    await asyncio.sleep(delay)
    await message.delete()


def encrypt_password(password: str) -> str:
    f = Fernet(config.crypto.key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode("utf-8")


def decrypt_password(password: str) -> str:
    f = Fernet(config.crypto.key)
    decrypted_password = f.decrypt(password)
    return decrypted_password.decode()
