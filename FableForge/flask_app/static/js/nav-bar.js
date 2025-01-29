const image = document.querySelector(".image")
const dropdown = document.querySelector(".dropdown_content")

image.onclick=function () {
    dropdown.classList.toggle("shown")
}