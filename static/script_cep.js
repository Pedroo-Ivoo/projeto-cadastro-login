       
function mostrarSenha(){
    let inputSenha = document.getElementById("senha");
    let btnExibeSenha = document.getElementById("btn-senha");

    if(inputSenha.type === 'password'){
        inputSenha.setAttribute("type", "text");
        btnExibeSenha.classList.replace("bi-eye", "bi-eye-slash");
    } else{
        inputSenha.setAttribute("type","password")
        btnExibeSenha.classList.replace("bi-eye-slash", "bi-eye");
    }
}