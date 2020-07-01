let logout = document.querySelector(".logout-config");

logout.addEventListener("click", function(){

    let xhr = new XMLHttpRequest();

    xhr.open("GET", "/api/sair");

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            window.location.href = "/entrar";
        }else{
            alert("Falha ao sair");
        }

    });

    xhr.send();

});

let submit = document.querySelector(".submit-config");

submit.addEventListener("click", function(event){
    event.preventDefault();

    init();

});

async function init(){
    const id = await carregaIdUsuario();
    
    console.log(id);

    atualizaUsuario(id);
    
}

window.onload = exibeId;

function exibeId(){
    let usuId = document.querySelector("#id");
    usuId.innerHTML = "ID de usuário: "+carregaIdUsuario();
}

function carregaIdUsuario(){
   
    let xhr = new XMLHttpRequest();

    let id=null;

    xhr.open("GET", "/api/get/me", false);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            let usuario = JSON.parse(resposta);
            console.log( usuario, usuario["usu_id"], usuario.usu_id)
            id = usuario["usu_id"];

        }else{
           console.log("deu errado");  
           id = null;         
        }

      
    });

    xhr.send();

    return id;
}

function atualizaUsuario(id){
    
    let form = document.querySelector("#form-config");

    let usuario = {}

    usuario["usu_id"] = id;
    if(form.usu_email.value.length > 0 ) usuario["usu_email"] = form.usu_email.value;
    if(form.usu_nome.value.length > 0 ) usuario["usu_nome"] = form.usu_nome.value;
    if(form.usu_senha.value.length > 0 ) usuario["usu_senha"] = form.usu_senha.value;
    
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/atualizar/usuario", false);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 202){
            alert("Mudança efetuada com sucesso");
            console.log(xhr.responseText);
            form.reset();
        }else{
            console.log(xhr.responseText);
            alert("Mudança falhou");
        }

    });

    xhr.send(JSON.stringify(usuario));
}