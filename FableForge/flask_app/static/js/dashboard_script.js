const flipButtons = document.querySelectorAll("button.btn")
const div1 = document.querySelector('')

flipButtons.forEach((button) => {
    button.onclick = function () {
        section.classList.toggle("flip-2")
    }
})

