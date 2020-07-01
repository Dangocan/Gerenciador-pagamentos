//retorna um objeto usuario
function carregaUsuario(){
   
    let xhr = new XMLHttpRequest();

    let usuario = null;

    xhr.open("GET", "/api/get/me");

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            usuario = JSON.parse(resposta);
            console.log(resposta);

        }else{
           console.log("deu errado");           
        }

      
    });

    xhr.send();
    
    return usuario;
}


// carregaUsuario if-> pega conta e pagamentos 

function carregaContas(){

    let xhr = new XMLHttpRequest();

    let contas = null;

    xhr.open("GET", "/api/get/contas");

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            contas = JSON.parse(resposta);
            console.log(resposta);

        }else{
           console.log("erro na requisicao de contas");           
        }

      
    });

    xhr.send();
    return contas;

}

function carregaPagamentos(){
   
    let xhr = new XMLHttpRequest();

    let pagamentos = null;

    xhr.open("GET", "/api/get/contas");

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            pagamentos = JSON.parse(resposta);
            console.log(resposta);

        }else{
           console.log("erro na requisicao de contas");           
        }

      
    });

    xhr.send();
    return pagamentos;
}

window.onload = init;

async function init(){
    //colocar processos com await aki que serao carregados ao carregar a pagina
    const usuario = await carregaUsuario();
    const contas = await carregaContas();
    const pagamentos = await carregaPagamentos();
    const divisoes =  [];
    const dividas = [];
    const devedores = {};

   contas.forEach(function(conta){
       divisoes.push(conta["con_divisoes"]);
    });
    
    divisoes.forEach(function(divisao){
        if(divisao["usu_object"] == usuario){
            dividas.push(divisao["div_valor"]);
        } else{
            devedores.push(divisao["div_valor"]);
            devedores.push(divisao["usu_object"]);
        }

    });

    console.log(divisoes);
    console.log(dividas);
    console.log(devedores);
    
    //processos de calculo
   // calculaDividas();

   // calculaDevedores();
    
    //processos de manipulação de html

}