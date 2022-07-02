from jwt   import encode, decode
from jwt import exceptions
from os    import getenv
from datetime import datetime, timedelta
from flask import jsonify

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

def write_token(data:dict):
    token = encode(payload={**data}, key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")
    
def valid_token(token, output=False):
    try:
        if output:
            return decode(token,key=getenv("SECRET"), algorithms=´["HS256"])
    except exceptions.DecodeError:
        reponse = jsonify({"message":"Invalid Token"})
        reponse.status_code = 401
        return reponse
    except exceptions.ExpiredSignatureError:
        reponse = jsonify({"message":"Token Expired"})
        reponse.status_code = 401
        return reponse