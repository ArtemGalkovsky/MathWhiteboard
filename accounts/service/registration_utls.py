from string import digits
from random import choices
from django.core.cache import cache
from MathWhiteboard.config import (ACCOUNTS_REGISTRATION_CODE_LIFE_SECONDS_IN_CACHE,
                                   ACCOUNTS_REGISTRATION_CODE_REQUEST_EMAIL_KEY_IN_CACHE,
                                   ACCOUNTS_REGISTRATION_CODE_LENGTH)
from hmac import new as hmac_new
from hashlib import sha256

from MathWhiteboard.settings import SECRET_KEY


def generate_new_code() -> str:
    return "".join(choices(digits, k=ACCOUNTS_REGISTRATION_CODE_LENGTH))

def get_hash_from_email(email: str) -> str:
    return hmac_new(SECRET_KEY.encode("UTF-8"), email.encode("UTF-8"), sha256).hexdigest()

def save_registration_code_to_cache(hashed_email: str, code: str) -> None:
    """
    :param hashed_email: str - User hashed email
    :param code: str - Registration code 
    :return: None
    """
    cache.set(
        ACCOUNTS_REGISTRATION_CODE_REQUEST_EMAIL_KEY_IN_CACHE.format(hashed_email=hashed_email),
        code,
        ACCOUNTS_REGISTRATION_CODE_LIFE_SECONDS_IN_CACHE
    )

def get_registration_code_from_email(hashed_email: str) -> str:
    return cache.get(ACCOUNTS_REGISTRATION_CODE_REQUEST_EMAIL_KEY_IN_CACHE.format(hashed_email=hashed_email))

def compare_registration_codes(hashed_email: str, code: str) -> bool:
    return get_registration_code_from_email(hashed_email) == code

