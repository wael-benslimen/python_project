const main = document.querySelector(".main");
// search_input
// search-button
// friend_section
const search_input = document.querySelector(".search_input");
const search_button = document.querySelector(".search-button");
const friend_section = document.querySelector(".friend_section");
search_button.addEventListener('click', async () => {
    await search_user();
});
async function search_user() {
    const response = await fetch('/friend/by-name/' + search_input.value);
    const data = await response.json();
    const { friends } = data
    friend_section.innerHTML = '';
    if (friends) {
        for (let i = 0; i < friends.length; i++) {
            const friend = document.createElement('div');
            friend.style = "border-radius: 10px;box-shadow: 0 0 10px rgba(0,0,0,0.1)"
            friend.innerHTML = `
                <div class="w-100 d-flex flex-column gap-2 align-items-center p-2">
                    <img src="${friends[i].image ? friends[i].image : '../placeholders/User_cicrle.png'}" alt="${friends[i].username}" width="50" height="50" style="border-radius: 50%">
                    <p>${friends[i].username}</p>
                </div>
                <div class="d-flex card-body flex-row gap-2">
                    <a href='/friend/{{friend.id}}'><i class="fa-solid fa-xl fa-user"></i></a>
                    <a href=''><i class="fa-solid fa-xl fa-envelope"></i></a>
                    <a href=''><i class="fa-solid fa-xl fa-trash-can"></i></i></a>
                </div>
            `
            friend_section.appendChild(friend);
        }
    }
}