import typing


def __make_list(*args: str, join_with: str, add_colon: bool = False, add_back_quote: bool = False) -> str:
    assert type(join_with) is str
    assert type(add_colon) is bool
    assert type(add_back_quote) is bool
    return join_with.join([f"{'`' if add_back_quote else ''}{':' if add_colon else ''}{str(arg)}{'`' if add_back_quote else ''}" for arg in args])


def _make_comma(*args: str, add_colon: bool = False, add_back_quote: bool = False) -> str:
    return __make_list(*args, join_with=", ", add_colon=add_colon, add_back_quote=add_back_quote)


def _make_and(*args: str, add_colon: bool = False, add_back_quote: bool = False) -> str:
    return __make_list(*args, join_with=" AND ", add_colon=add_colon, add_back_quote=add_back_quote)


def __make_equal(*args: str, join_with: str) -> str:
    assert type(join_with) is str
    return join_with.join([f"`{arg}` = :{arg}" for arg in args])


def _make_equal_where(*args: str) -> str:
    return __make_equal(*args, join_with=" AND ")


def _make_equal_set(*args: str) -> str:
    return __make_equal(*args, join_with=", ")


def make_insert(*args: str, t_name: str) -> str:
    return F"""INSERT INTO `{t_name}` ({_make_comma(*args, add_back_quote=True)}) VALUES ({_make_comma(*args, add_colon=True)})"""


def make_select(*args: str, t_name: str) -> str:
    return F"""SELECT * FROM `{t_name}` WHERE {_make_equal_where(*args)}"""


def make_update(*, set_list: typing.List[str], where_list: typing.List[str], t_name: str) -> str:
    return F"""UPDATE `{t_name}` SET {_make_equal_set(*set_list)} WHERE {_make_equal_where(*where_list)}"""


def make_delete(*args: str, t_name: str) -> str:
    return F"""DELETE FROM `{t_name}` WHERE {_make_equal_where(*args)}"""


if __name__ == "__main__":
    pass
