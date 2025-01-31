const signUpBtnLink = document.querySelector('.signUpBtn-link');
const signInBtnLink = document.querySelector('.signInBtn-link');
const wrapper = document.querySelector('.wrapper');
async function handleSignup(){
    try {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const email = document.getElementById('email').value;
        const file = document.getElementById('file').files[0];
        const avatar = await handleFileReading(file);
        const data = {username, password, email,avatar};
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if(response.ok){
            const {token} = await response.json();
            localStorage.setItem('token', token);
            window.location.href = '/dashboard';
        }
    } catch (error) {
        alert('Signup failed');
        
    }
}

function handleFileReading(file){
    return new Promise((resolve,reject)=>{
        if(file && file instanceof File){
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (event) => {
                if(reader.result){
                    resolve(reader.result);
                }
            };
            reader.onerror = function(){
                reject(new Error('Error reading file'));
            }
        }
    })
}

signUpBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active')
})

signInBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active')
})