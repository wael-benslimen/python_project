const profile = document.querySelector(".profile");
const friend = document.querySelector(".friend");
const main = document.querySelector(".main");


profile.addEventListener('click', () => {
    main.classList.toggle('active');
});

friend.addEventListener('click', () => {
    main.classList.toggle('active');
});