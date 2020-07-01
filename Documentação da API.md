# URLs de acesso da API
__Os parâmetros devem ser todos passados em forma de JSON__
## GET /api/get/usuarios *
Acesso as informações de todos os usuarios
#### Parâmetros necessários: 
- Nenhum
#### Respostas:
- 200: [Usuario[object]]
- 400/401/404: Resposta[object]

## GET /api/get/usuario/{usu_id} *
Acesso as informações de um usuário pelo seu id
#### Parâmetros necessários: 
- Nenhum
#### Respostas:
- 200: Usuario[object]
- 400/401/404: Resposta[object]

## POST /api/entrar
Realiza login do usuário
#### Parâmetros necessários: 
- usu_email
- usu_senha
#### Respostas:
- 200: Usuario[object]
- 400: Resposta[object]

## GET /api/get/me *
Informações do usuário
#### Parâmetros necessários: 
- Nenhum
#### Respostas:
- 200: [Usuario[object]]
- 400/401/404: Resposta[object]

## GET /api/sair
Realiza o logout do usuário
#### Parâmetros necessários: 
- Nenhum
#### Respostas:
- 200: Resposta[object]

## GET /api/get/contas *
Pegar as contas das quais o usuário da sessão tem participação
#### Parâmetros necessários:
- usu_email
- usu_senha
#### Respostas:
- 200: [Contas[object]
- 400/401/404: Resposta[object]

## GET /api/get/pagamentos *
Pegar pagamentos do qual o usuário da sessão tem participação
#### Parâmetros necessários:
- Nenhum
#### Respostas:
- 200: [Pagamento[object]]
- 400/401/404:  Resposta[object]

## POST /api/cadastrar/usuario
#### Parâmetros necessários:
- usu_email
- usu_senha
- usu_nome
#### Respostas:
- 201: Usuario[object]
- 400: Resposta[object]

## POST /api/cadastrar/conta *
Cadastrar conta
#### Parâmetros necessários:
- con_titulo
- con_descricao
- usu_id
- con_divisoes: [{usu_id, div_valor}]
#### Respostas:
- 201: Conta[object]
- 400/401/404: Resposta[object]

## POST /api/cadastrar/pagamento *
Cadastrar um pagamento
#### Parâmetros necessários:
- usu_pagador_id
- usu_receptor_id
- pag_valor
- pag_mensagem
#### Respostas:
- 201: Conta[object]
- 400/401/404: Resposta[object]

## POST /api/atualizar/usuario *
Realizar atualização de informações do usuário
#### Parâmetros necessários:
- usu_id
#### Parâmetros opcionais:
Informe os campos que deseja realizar a alteração
- usu_email
- usu_nome
- usu_senha
#### Respostas:
- 202: Usuario[object]
- 400/401/403/404: Resposta[object]



__\*Obrigatório login__            
## Objetos de respostas
    Usuario[object]
    {
        usu_id:       INTEGER
        usu_email:    TEXT
        usu_nome:     TEXT
        usu_datahora: TEXT
    }
    
    Conta[object]
    {
       con_id:        INTEGER
	   usu_id: 		  INTEGER
       con_titulo:    TEXT
       con_descricao: TEXT    NULL,
       con_datahora:  TEXT
       con_divisoes:  [Divisao[object]]
	   usu_object:    Usuario[object]
    }

    Divisao[object]
    {
        div_id:    INTEGER
        con_id:    INTEGER
        usu_id:    INTEGER
        div_valor: REAL
		usu_object: Usuario[object]
    }

    Pagamento[object]
    {
        pag_id:                 INTEGER
		usu_pagador_id:         INTEGER
        usu_receptor_id:        INTEGER
        pag_valor:              REAL
        pag_mensagem:           TEXT    NULL
        pag_datahora:           TEXT
		usu_pagador_object:     Usuario[object]
        usu_receptor_object:    Usuario[object]
    }

    Resposta[object]
    {
        mensagem: TEXT,
        [informação extra que pode ajudar a encontrar erros]
    }
