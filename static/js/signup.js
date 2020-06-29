let submit = document.querySelector(".submit");

submit.addEventListener("click", function(event){
    event.preventDefault();

    var form = document.querySelector("#form-cadastro");

    var usuario = obtemUsuarioDoFormulario(form);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/api/cadastrar/usuario", true);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 201){

            window.location.href = "/resumo"

        }else{
           alert("falha ao cadastrar usuario");
           form.reset();
        }

      
    });

    xhr.send(usuario);

});

function obtemUsuarioDoFormulario(form){
    var usuario = {
        usu_email: form.usu_email.value,
        usu_senha: form.usu_senha.value,
        usu_nome: form.usu_nome.value
    }

    return JSON.stringify(usuario);
}