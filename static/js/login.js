var submit = document.querySelector(".submit");

var logado = false;

submit.addEventListener("click", function(event){
    event.preventDefault();

    var form = document.querySelector("#form-login");

    var usuario = obtemUsuarioDoFormulario(form);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/api/entrar", true);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            logado = true;
            window.location.href = "/resumo"

        }else{
           logado = false;
           alert("usuario e/ou senha invalidos");
           form.reset();
        }

      
    });

    xhr.send(usuario);

});

function obtemUsuarioDoFormulario(form){
    var usuario = {
        usu_email: form.usu_email.value,
        usu_senha: form.usu_senha.value,
    }

    return JSON.stringify(usuario);
}

