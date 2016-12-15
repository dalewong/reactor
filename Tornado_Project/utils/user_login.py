import functools
from utils.response_code import RET
from session import Session

def user_login(func):
    @functools.wraps(func)
    def wrapper(requestHandler, *args, **argv):
        usr_session = Session(requestHandler)
        # usr_session = session.data
        # usr_session = requestHandler.get_secure_cookie('session_id')
        if usr_session:
            return func(requestHandler, usr_session, *args, **argv)

        return requestHandler.write(dict(erron=RET.SESSIONERR, errmsg ="/login.html" ))

    return wrapper

