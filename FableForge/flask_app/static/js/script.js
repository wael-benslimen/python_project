const eyes = document.querySelectorAll(".fa-solid")
const password_inputs = document.querySelectorAll("input[type='password']")
const section = document.querySelector("section.login-register")
const flipButtons = document.querySelectorAll("button.flip-1")
eyes.forEach((eye)=>{
    eye.onclick = function() {
        for(var i = 0; i<password_inputs.length; i++){
            if (password_inputs[i].type == "text") {
                password_inputs[i].type = "password"
                eye.classList.replace("fa-eye","fa-eye-slash")
            } else {
                password_inputs[i].type = "text"
                eye.classList.replace("fa-eye-slash","fa-eye")
            }
        }
    }
})
flipButtons.forEach((button)=>{
    button.onclick = function() {
        section.classList.toggle("flip-2")
    }
})