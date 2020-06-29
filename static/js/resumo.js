let usuario;

function carregaUsuario(){
   
    let xhr = new XMLHttpRequest();

    xhr.open("GET", "/api/get/me");

    xhr.addEventListener("load", function(){
        
        if(xhr.status == 200){
            let resposta = xhr.responseText;
            usuario = JSON.parse(resposta);
            console.log(resposta);
            return usuario;

        }else{
           console.log("deu errado");  
           return null;         
        }

      
    });

    xhr.send();
}

// carregaUsuario if-> pega conta e pagamentos 

function carregaDadosDeContas(usuario){



}

window.onload = carregaUsuario;