
function validateLoginForm() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("error-message");

    let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    errorMessage.style.display = "none";
    errorMessage.innerHTML = "";

    if (!email && !password) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "All fields are required.";
        return false;
    }
    if (!email.match(emailPattern)) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Please enter a valid email address.";
        return false;  
    }

    if (!password) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Password cannot be empty.";
        return false; 
    }

    return true;
}

function validateRegisterForm() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let phone = document.getElementById('phone').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById("password").value;
    let confirm_password = document.getElementById('confirm_password').value;
    let errorMessage = document.getElementById("error-message");

    let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    let errors = [];
    errorMessage.style.display = "none";
    errorMessage.innerHTML = "";

    if (!name && !email && !password&& !username) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "All fields are required.";
        return false;
    }

    if (!name) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Name cannot be empty.";
        return false;
    }

    if (!username) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Username cannot be empty.";
        return false;
    }


    if (!email.match(emailPattern)) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Please enter a valid email address.";
        return false;  
    }
    if (!phone) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Phone cannot be empty.";
        return false; 
    }

    if (!password) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Password cannot be empty.";
        return false; 
    }
    if (!confirm_password) {
        errorMessage.style.display = "block";
        errorMessage.innerHTML = "Confirm Password cannot be empty.";
        return false; 
    }

    return true;
}