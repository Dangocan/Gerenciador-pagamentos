var submit = document.querySelector(".submit");

submit.addEventListener("click", function(event){
   
    event.preventDefault();

    var form = document.querySelector("#form-pag");

    var pagamento = obtemDadosDoFormulario(form);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/api/cadastrar/pagamento", true);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 201){
            alert("pagamento realizado com sucesso!");
            form.reset();

        }else{
           alert("pagamento falhou");
           form.reset();
        }

      
    });

    xhr.send(pagamento);

});

function obtemDadosDoFormulario(form){
    var pagamento = {
        usu_pagador_id: form.usu_pagador_id.value,
        usu_receptor_id: form.usu_receptor_id.value,
        pag_valor: form.pag_valor.value,
        pag_mensagem: form.pag_mensagem.value
    }

    return JSON.stringify(pagamento);
}

