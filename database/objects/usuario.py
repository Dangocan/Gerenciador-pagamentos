from __future__ import annotations
import typing
from datetime import datetime
import database.utils
import database
import settings
import utils
import secrets
import hashlib
from errors import KnownError


class UserError(KnownError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message, status)


class UserUpdateForbiddenError(UserError):
    def __init__(self, *, usu_id_requester, usu_id_update):
        self.usu_id_requester = usu_id_requester
        self.usu_id_update = usu_id_update
        super().__init__("Usuário não tem permissao para atualizar", 403)


class UserIDNotFoundError(UserError):
    def __init__(self, *, usu_id):
        self.usu_id = usu_id
        super().__init__("Usuário não encontrado", 404)


class UserEmailNotFoundError(UserError):
    def __init__(self, *, usu_email):
        self.usu_email = usu_email
        super().__init__("Usuário não encontrado", 404)


class InvalidUserPassword(UserError):
    def __init__(self, message: str):
        super().__init__(f"Senha inválida: {message}", 400)


class InvalidUserEmail(UserError):
    def __init__(self, message: str):
        super().__init__(f"Email inválido: {message}", 400)


class InvalidUserName(UserError):
    def __init__(self, message: str):
        super().__init__(f"Nome inválido: {message}", 400)


class WrongPasswordFromEmailError(UserError):
    def __init__(self, *, usu_email: str):
        self.usu_email = usu_email
        super().__init__(f"Senha incorreta", 400)


class LoginGenericUserAuthenticationError(UserError):
    def __init__(self):
        super().__init__(f"Email e/ou senha incorreto(s)", 400)


def hash_password(password: str, salt: str = None) -> typing.Tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(20)
    hashed_password = hashlib.sha256((salt + password).encode("UTF-8")).hexdigest()
    return hashed_password, salt


def validar_email(email: str):
    if email == "":
        raise InvalidUserEmail("vazio")


def validar_senha(password: str):
    if type(password) is not str:
        raise InvalidUserPassword("não é do tipo texto")
    if password == "":
        raise InvalidUserPassword("vazio")


def validar_nome(name: str):
    if type(name) is not str:
        raise InvalidUserName("não é do tipo texto")
    if name == "":
        raise InvalidUserName("vazio")


class Usuario:
    def __init__(self, usu_id: int, usu_email: str, usu_nome: str, usu_senha: str, usu_salt: str, usu_datahora: str):
        self.usu_id = usu_id
        self.usu_email = usu_email
        self.usu_nome = usu_nome
        self.usu_senha = usu_senha
        self.usu_salt = usu_salt
        self.usu_datahora = usu_datahora

    def __eq__(self, other: typing.Union[Usuario, int, str]):
        if type(other) is Usuario:
            return str(self.usu_id) == str(other.usu_id)
        else:
            return str(self.usu_id) == str(other)

    def __repr__(self):
        return f"""<Usuario {self.usu_id} {self.usu_email} {self.usu_nome} {self.usu_datahora}>"""

    def json(self) -> dict:
        return {
            "usu_id": self.usu_id,
            "usu_email": self.usu_email,
            "usu_nome": self.usu_nome,
            "usu_datahora": self.usu_datahora
        }

    @classmethod
    def new(cls, *, usu_email: str, usu_nome: str, usu_senha: str) -> Usuario:
        logger.debug("New user")
        validar_email(usu_email)
        validar_nome(usu_nome)
        validar_senha(usu_senha)
        usu_datahora = datetime.utcnow().strftime(settings.STDDATETIMEFORMAT)
        usu_senha, usu_salt = hash_password(usu_senha)
        object_dict = {"usu_email": usu_email, "usu_nome": usu_nome, "usu_senha": usu_senha, "usu_datahora": usu_datahora, "usu_salt": usu_salt}

        with database.Database() as db:
            sql_insert = database.utils.make_insert("usu_email", "usu_nome", "usu_senha", "usu_salt", "usu_datahora", t_name="usuario")
            usu_id = db.insert(sql_insert, **object_dict)

            sql_select = database.utils.make_select("usu_id", t_name="usuario")
            return cls(**db.select(sql_select, usu_id=usu_id)[0])

    @classmethod
    def update(cls, *, usuario: Usuario, usu_id: typing.Union[int, str], usu_email: str = None, usu_nome: str = None, usu_senha: str = None) -> Usuario:
        logger.debug("Update user")
        if usuario != usu_id:
            raise UserUpdateForbiddenError(usu_id_requester=usuario.usu_id, usu_id_update=usu_id)

        updates = {"usu_id": usu_id}

        if usu_email is not None:
            validar_email(usu_email)
            updates["usu_email"] = usu_email

        if usu_nome is not None:
            validar_nome(usu_nome)
            updates["usu_nome"] = usu_nome

        if usu_senha is not None:
            validar_senha(usu_senha)
            updates["usu_senha"], updates["usu_salt"] = hash_password(usu_senha)

        with database.Database() as db:
            sql_update = database.utils.make_update(where_list=["usu_id"], set_list=list(updates.keys()), t_name="usuario")
            db.update(sql_update, **updates)

            sql_select = database.utils.make_select("usu_id", t_name="usuario")
            return cls(**db.select(sql_select, usu_id=usu_id)[0])

    @classmethod
    def get_by_id(cls, usu_id):
        try:
            return cls.get(sql_select=database.utils.make_select("usu_id", t_name="usuario"), values={"usu_id": usu_id})[0]
        except IndexError:
            raise UserIDNotFoundError(usu_id=usu_id)

    @classmethod
    def get_by_email(cls, usu_email):
        try:
            return cls.get(sql_select=database.utils.make_select("usu_email", t_name="usuario"), values={"usu_email": usu_email})[0]
        except IndexError:
            raise UserEmailNotFoundError(usu_email=usu_email)

    @classmethod
    def get_all(cls):
        return cls.get(sql_select=F"""SELECT * FROM `usuario`""", values={})

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Usuario]:
        with database.Database() as db:
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    @classmethod
    def authenticate_login(cls, usu_email: str, usu_senha: str) -> Usuario:
        try:
            logger.debug(f"Authenticate user with email: {usu_email}")
            user = cls.get_by_email(usu_email=usu_email)
            if user.usu_senha == hash_password(usu_senha, user.usu_salt)[0]:
                logger.debug("Authenticated")
                return user
            else:
                logger.debug("Wrong password")
                raise WrongPasswordFromEmailError(usu_email=usu_email)
        except (WrongPasswordFromEmailError, UserEmailNotFoundError):
            raise LoginGenericUserAuthenticationError()


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
    # u = Usuario.new(usu_email="a@a.com", usu_nome="a", usu_senha="senha")
    # u = Usuario.new(usu_email="b@b.com", usu_nome="b", usu_senha="senhb")
    # u = Usuario.get_by_id("1")
    # print(u != 0)
    # u = Usuario.update(usu_id=1, usu_nome="jonasi")
    # print(u)
    # print(hash_password("alex", "039df246fbdb0a54611af4a5411188d729c8d7d5")[0] == "180f7811021dad67cffefc1155f0e0a41167d910d749ad5d48927f4b5894fe19")
