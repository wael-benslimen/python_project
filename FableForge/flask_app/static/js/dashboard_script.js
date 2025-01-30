const section1 = document.querySelector('.quest_create')
const section2 = document.querySelector('.quest_view')
const btn = document.querySelector('.plus_btn')
const image = document.querySelector(".gear")
const dropdown = document.querySelector(".dropdown_menu")
const description = document.querySelectorAll(".card_info")


function toggleClass() {
    section1.classList.toggle("hidden_face")
    section2.classList.toggle("hidden_face")
    btn.classList.toggle("rotate_btn")
}

image.onclick = function () {
    dropdown.classList.toggle("show")
}
description.forEach(item => {
    item.onclick = function () {
        item.classList.toggle('show_description')
    }
});


