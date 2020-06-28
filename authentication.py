from functools import wraps
from flask import session, g, redirect, url_for
import utils
from database.objects import Usuario
from responses import resposta
from errors import *


def authenticate(f):
    @wraps(f)
    def auth_wrapper(*args, **kwargs):
        if "usu_id" in session:
            try:
                g.usuario = Usuario.get_by_id(session["usu_id"])
            except IndexError:
                logger.debug("User not found")
            except Exception as e:
                logger.exception(e)
            else:
                return f(*args, **kwargs)
        return redirect(url_for("page_entrar"))

    return auth_wrapper


def unauthenticate(f):
    @wraps(f)
    def unauth_wrapper(*args, **kwargs):
        session.pop("usu_id", None)
        g.usuario = None
        return f(*args, **kwargs)

    return unauth_wrapper


def authenticate_api(f):
    @wraps(f)
    def auth_api_wrapper(*args, **kwargs):
        try:
            if "usu_id" in session:
                g.usuario = Usuario.get_by_id(session["usu_id"])
            else:
                raise UserNotLoggedInError()
        except KnownError as e:
            return resposta(e)
        except Exception as e:
            logger.exception(e)
            return resposta("Um erro desconhecido ocorreu", 400)
        else:
            return f(*args, **kwargs)

    return auth_api_wrapper


logger = utils.get_logger(__file__)
