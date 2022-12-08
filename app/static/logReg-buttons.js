//alert("hello");
const registerButton = document.querySelector(".registerBtn");
const loginButton = document.querySelector(".loginBtn");
const moveButton = document.querySelector(".moveBtn");
const loginForm = document.querySelector(".loginForm");
const registerForm = document.querySelector(".registerForm");

registerButton.addEventListener("click", ()=>{
    moveButton.classList.add("rightBtn");
    loginForm.classList.add("hideForm")
    registerForm.classList.remove("hideForm")
    moveButton.innerHTML = "Register";
})

loginButton.addEventListener("click", ()=>{
    moveButton.classList.remove("rightBtn");
    loginForm.classList.remove("hideForm");
    registerForm.classList.add("hideForm");
    moveButton.innerHTML = "Login";
})

