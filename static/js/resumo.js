Promise.all([
    fetch("/api/get/contas").then(r => r.json()),
    fetch("/api/get/pagamentos").then(r => r.json()),
    fetch("/api/get/me").then(r => r.json())
])
.then(function ([contas, pagamentos, usuario]) {
    //cole aqui o codigo anterior meu
    let resumo = {};
    let usuario_id = usuario["usu_id"];
    for (let conta of contas) {
        // para cada conta fazer:
        let pagador_id = conta["usu_id"]; // quem pagou a conta
        let divisoes = conta["con_divisoes"]; // pegar as divioes
        for (let divisao of divisoes) {
            // para cada divisao fazer:
            if (divisao["usu_id"] === pagador_id) continue; // a pessoa que pagou é a mesma da divisão atual, seguir
            if (usuario_id === pagador_id) {
                // usuario é o pagador
                resumo[divisao["usu_id"]] = (resumo[divisao["usu_id"]] || 0) + divisao["div_valor"]; //usuario recebe credito
            } else {
                // usuario não é o pagador
                if (divisao["usu_id"] !== usuario_id) continue; // divisao na qual o usuario não faz parte
                resumo[conta["usu_id"]] = (resumo[conta["usu_id"]] || 0) - divisao["div_valor"]; //usuario tem que pagar para o pagador
            }
        }
    }

    for (let pagamento of pagamentos) {
        // para cada pagamento fazer:
        if (pagamento["usu_pagador_id"] === pagamento["usu_receptor_id"]) {
            console.log(pagamento);
            console.warn("Pagamento feito para mesma pessoa");
            continue;
        }
        if (pagamento["usu_pagador_id"] === usuario_id) {
            // usuario que fez o pagamento
            resumo[pagamento["usu_receptor_id"]] = (resumo[pagamento["usu_receptor_id"]] || 0) + pagamento["pag_valor"];
        } else if (pagamento["usu_receptor_id"] === usuario_id) {
            // usuario recebeu o pagamento
            resumo[pagamento["usu_pagador_id"]] = (resumo[pagamento["usu_pagador_id"]] || 0) - pagamento["pag_valor"];
        } else continue; //usuario não participou do pagamento
    }
    console.log(resumo);

    //codigo dangocan:
    Object.keys(resumo).forEach(function (usu_id){
       
        console.log(Object.keys(resumo)) // [1, 57];        
        
        if(resumo[usu_id] > 0){
            let ul = document.querySelector("#devedores");
            let li = document.createElement("li");
            li.classList.add("resumo-item");
            li.innerHTML = `Usuario de ID: ${usu_id} te deve: ${resumo[usu_id]}`;
            ul.appendChild(li);
        }
        
        if(resumo[usu_id] < 0){
            let ul = document.querySelector("#dividas");
            let li = document.createElement("li");
            li.classList.add("resumo-item");
            li.innerHTML = `Voce deve: ${Math.abs(resumo[usu_id])} ao usuário de ID: ${usu_id}`;
            ul.appendChild(li);
        }
    });
});