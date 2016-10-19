import functools
import logging

LOG = logging.getLogger()

def auth_required(method):
    '''
    require the user to be logged in
    '''
    @functools.wraps(method)
    def wrapper(handler, *args, **kwargs):
        if not handler.current_user_id:
            LOG.error("*[Auth_Required]* IP:%s PATH:%s Cookies:%s UA:%s",
                      handler.get_ip(),
                      handler.request.path,
                      handler.request.headers.get("Cookie", None),
                      handler.request.headers.get("User-Agent", None))
            return handler.send_error(401, reason="login first")
        else:
            return method(handler, *args, **kwargs)
    return wrapper

