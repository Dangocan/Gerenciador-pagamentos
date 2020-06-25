CREATE TABLE IF NOT EXISTS usuario
(
    usu_id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- id unico do usuario
    usu_email    TEXT    NOT NULL UNIQUE,                    -- email do usuario
    usu_nome     TEXT    NOT NULL,                           -- nome completo do usuario
    usu_senha    TEXT    NOT NULL,                           -- senha em hash (com salt) do usuario
    usu_salt     TEXT    NOT NULL,                           -- salt (aleatorio) do usuario
    usu_datahora TEXT    NOT NULL                            -- criacao data e hora %Y-%m-%d %H:%M:%S
);

CREATE TABLE IF NOT EXISTS conta
(
    con_id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- id da conta 
    usu_id        INTEGER NOT NULL,                           -- id do usuario pagador da conta
    con_titulo    TEXT    NOT NULL,                           -- titulo da conta
    con_descricao TEXT    NULL,                               -- descrição da conta
    con_datahora  TEXT    NOT NULL,                           -- cricao data e hora %Y-%m-%d %H:%M:%S
    FOREIGN KEY (usu_id) REFERENCES usuario (usu_id)
);

CREATE TABLE IF NOT EXISTS divisao
(
    div_id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- id da divisao
    con_id    INTEGER NOT NULL,                           -- id da conta da qual a divisao pertence
    usu_id    INTEGER NOT NULL,                           -- id do usuario da qual a divisao pertence
    div_valor REAL    NOT NULL,                           -- valor a ser pago pelo usuario
    FOREIGN KEY (con_id) REFERENCES conta (con_id),
    FOREIGN KEY (usu_id) REFERENCES usuario (usu_id)
);

CREATE TABLE IF NOT EXISTS pagamento
(
    pag_id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- id do pagamento
    usu_pagador_id  INTEGER NOT NULL,                           -- id do usuario pagador
    usu_receptor_id INTEGER NOT NULL,                           -- id do usuario a receber
    pag_valor       REAL    NOT NULL,                           -- valor pago
    pag_mensagem    TEXT    NULL,                               -- mensagem de pagamento
    pag_datahora    TEXT    NOT NULL,                           -- data e hora do pagamento
    FOREIGN KEY (usu_pagador_id) REFERENCES usuario (usu_id),
    FOREIGN KEY (usu_receptor_id) REFERENCES usuario (usu_id)
);
