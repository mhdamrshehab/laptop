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
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById('phone').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById('confirm_password').value;


    let nameError = document.getElementById("name-error");
    let emailError = document.getElementById("email-error");
    let phoneError = document.getElementById("phone-error");
    let usernameError = document.getElementById("username-error");
    let passwordError = document.getElementById("password-error");
    let confirmPasswordError = document.getElementById("confirm_password-error");
    let count = 0;

    nameError.innerHTML = "";
    emailError.innerHTML = "";
    phoneError.innerHTML = "";
    usernameError.innerHTML = "";
    passwordError.innerHTML = "";
    confirmPasswordError.innerHTML = "";

    let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (!name) {
        nameError.innerHTML = "Name cannot be empty.";
        count++;
    }

    if (!username) {
        usernameError.innerHTML = "Username cannot be empty.";
        count++;
    }

    if (!email.match(emailPattern)) {
        emailError.innerHTML = "Please enter a valid email address.";
        count++;
  
    }
    if (!phone) {
        phoneError.innerHTML = "Phone number cannot be empty.";
        count++;
 
    }
    if (isNaN(phone)) {
        phoneError.innerHTML = "Phone number must contain numbers only.";
        count++;
    }

    if (!password) {
        passwordError.innerHTML = "Password cannot be empty.";
        count++;
 
    }
    if (!confirm_password) {
        confirmPasswordError.innerHTML = "Confirm Password cannot be empty.";
        count++;
 
    }
    if (password != confirm_password) {
        confirmPasswordError.innerHTML = "Passwords do not match.";
        count++;

    }

    if(count>0){
        return false}
    return true;
}