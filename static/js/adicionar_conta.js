let submit = document.querySelector(".submit");
let botaoAdicionaDivisao = document.querySelector("#nova-divisao");
let botaoExcluiDivisao = document.querySelector("#exclui-divisao");
let contadorDivisoes = 1;

submit.addEventListener("click", function(event){
    event.preventDefault();

    var form = document.querySelector("#form-add");

    var conta = obtemContaDoFormulario(form, contadorDivisoes);

    console.log(conta);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/api/cadastrar/conta", true);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 201){
            alert("conta adicionada com sucesso!");
            form.reset();

        }else{
           alert("Falha ao adicionar conta");
        }

      
    });

    console.log(conta);

    xhr.send(JSON.stringify(conta));

});

botaoAdicionaDivisao.addEventListener("click", function(){
    
    console.log("fuiclicado");
    contadorDivisoes++;
    let divisoes = document.querySelector("#divisoes");

    let label = document.createElement("label");
    label.textContent = "ID de usuario";
    divisoes.appendChild(label);

    let elt = document.createElement("input");
    elt.classList.add("input-padrao");
    elt.setAttribute("type", "text");
    elt.setAttribute("name", "usu_id"+contadorDivisoes);
    elt.setAttribute("required", true);
    elt.setAttribute("placeholder", "0000");
    divisoes.appendChild(elt);

    let label2 = document.createElement("label");
    label2.textContent = "Parte na divisão";
    divisoes.appendChild(label2);

    let elt2 = document.createElement("input");
    elt2.classList.add("input-padrao");
    elt2.setAttribute("type", "text");
    elt2.setAttribute("name", "div_valor"+contadorDivisoes);
    elt2.setAttribute("required", true);
    elt2.setAttribute("placeholder", "R$xx-xx");
    divisoes.appendChild(elt2);


});

botaoExcluiDivisao.addEventListener("click", function(){
    contadorDivisoes = 0;
    let divisoes = document.querySelector("#divisoes");
    divisoes.innerHTML = "";
});

function obtemContaDoFormulario(form, contadorDivisoes){
    var conta = {
        con_titulo: form.con_titulo.value,
        con_descricao: form.con_descricao.value,
        usu_id: carregaIdUsuario(),
        con_divisoes: []
    }

    for(let i = 1; i <= contadorDivisoes; i++){
        conta["con_divisoes"].push({usu_id: form[`usu_id${i}`].value, div_valor: form[`div_valor${i}`].value});
    }

    return conta;
}

function carregaIdUsuario(){
   
    let xhr = new XMLHttpRequest();

    let id=null;

    xhr.open("GET", "/api/get/me", false);

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            let usuario = JSON.parse(resposta);
            id = usuario["usu_id"];

        }else{
           console.log("deu errado");  
           id = null;         
        }

      
    });

    xhr.send();

    return id;
}