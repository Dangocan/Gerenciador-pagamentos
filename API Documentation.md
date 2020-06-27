URLs de acesso da API:
 
# GET /api/usuarios *
Acesso as informações de todos os usuarios
#### Parâmetros necessários: 
- Nenhum
#### Respostas:
- 200: [Usuario[object]]
- 400: Error[object]

# POST /api/entrar
Realiza login do usuário
#### Parâmetros necessários: 
- usu_email
- usu_senha
#### Respostas:
- 200: Usuario[object]
- 400: Error[object]

# GET /api/contas *
Realiza login do usuário
#### Parâmetros necessários:
- usu_email
- usu_senha
#### Respostas:
- 200: [Contas[object]
- 400: Error[object]

# GET /api/pagamentos *
Pegar pagamentos do usuario na sessão
#### Parâmetros necessários:
- Nenhum
#### Respostas:
- 200: [Pagamento[object]]
- 400:  Error[object]

# POST /api/cadastrar/usuario
#### Parâmetros necessários:
- usu_email
- usu_senha
- usu_nome
#### Respostas:
- 201: Usuario[object]
- 400: Error[object]

# POST /api/cadastrar/conta *
Cadastrar conta
#### Parâmetros necessários:
- con_titulo
- con_descricao
- usu_id
- con_divisoes: [div_id, usu_id, div_valor]
#### Respostas:
- 201: Conta[object]
- 400: Error[object]

# POST /api/cadastrar/pagamento *
Cadastrar um pagamento
#### Parâmetros necessários:
- usu_pagador_id
- usu_receptor_id
- pag_valor
- pag_mensagem
#### Respostas:
- 201: Conta[object]
- 400: Error[object]


\* Necessita de autenticação            
## Objetos de respostas
    Usuario[object]
    {
        usu_id:       INTEGER
        usu_email:    TEXT
        usu_nome:     TEXT
        usu_datahora: TEXT    NOT NULL
    }
    
    Conta[object]{
       con_id:        INTEGER
       usu_object:    Usuario[object]
       con_titulo:    TEXT
       con_descricao: TEXT    NULL,
       con_datahora:  TEXT
       con_divisoes:  [Divisao[object]]
    }

    Divisao[object]
    {
        div_id:    INTEGER
        con_id:    INTEGER
        usu_id:    INTEGER
        div_valor: REAL
    }

    Pagamento[object]
    {
        pag_id:                 INTEGER
        usu_pagador_object:     Usuario[object]
        usu_receptor_object:    Usuario[object]
        pag_valor:              REAL
        pag_mensagem:           TEXT    NULL
        pag_datahora:           TEXT
    }

    Resposta[object]{
        mensagem: TEXT
    }
