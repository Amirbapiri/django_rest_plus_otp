import os
from string import digits
from random import choice

from dotenv import load_dotenv

from kavenegar import *

from otp.models import Otp


load_dotenv()


def generate_code(size: int = 6, chars=digits):
    return "".join(choice(chars) for _ in range(size))


def otp_generator(size: int = 6) -> str:
    code = generate_code(size)
    is_otp_exists = Otp.objects.filter(otp=code).exists()
    if not is_otp_exists:
        return code
    return otp_generator(size)


def send_otp(phone, otp):
    try:
        api = KavenegarAPI(os.getenv("KAVENEGAR_API_KEY"))
        params = {
            "sender": "1000596446",  # optional
            "receptor": [
                phone,
            ],
            "message": f"Your OPT is: {otp}",
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
