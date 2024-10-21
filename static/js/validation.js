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

function validatePrdouctForm(){
    const title = document.getElementById("title").value;
    const category = document.getElementById("category").value;
    const model = document.getElementById("model").value;
    const brand = document.getElementById("brand").value;
    const color = document.getElementById("color").value;
    const quantity = document.getElementById("quantity").value;
    const price = document.getElementById("price").value;
    const offer_price = document.getElementById("offer_price").value;
    const description = document.getElementById("description").value;

    let titleError = document.getElementById("title-error");
    let categoryError = document.getElementById("category-error");
    let modelError = document.getElementById("model-error");
    let brandError = document.getElementById("brand-error");
    let colorError = document.getElementById("color-error");
    let quantityError = document.getElementById("quantity-error");
    let priceError = document.getElementById("price-error");
    let offerpriceError = document.getElementById("offerprice-error");
    let descriptionError = document.getElementById("description-error");
    let count = 0;

    if(!title)
    {
        titleError.innerHTML = "Title cannot be empty.";
        count++;
    }
    if(!category)
    {
        categoryError.innerHTML = "Category cannot be empty.";
        count++;
    }
    if(!model)
    {
        modelError.innerHTML = "Model cannot be empty.";
        count++;
    }
    if(!brand)
    {
        brandError.innerHTML = "Brand cannot be empty.";
        count++;
    }
    if(!color)
    {
        colorError.innerHTML = "Color cannot be empty.";
        count++;
    }
    if(!quantity)
    {
        quantityError.innerHTML = "Quantity cannot be empty.";
        count++;
    }
    if(isNaN(quantity))
    {
        quantityError.innerHTML = "Quantity must contain numbers only.";
        count++;
    }
    if(!price)
    {
        priceError.innerHTML = "Price cannot be empty.";
        count++;
    }
    if(isNaN(price))
    {
        priceError.innerHTML = "Price must contain numbers only.";
        count++;
    }
    if(isNaN(offer_price))
    {
        offerpriceError.innerHTML = "Offer Price must contain numbers only.";
        count++;
    }
    if(!description)
    {
        descriptionError.innerHTML = "Description cannot be empty.";
        count++;
    }


    if(count>0){
        return false}
    return true;

}

function validateEditProfileForm(){
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
    
    
    if (!email) {
        emailError.innerHTML = "Email cannot be empty.";
        count++;
    }
    

    if (!email.match(emailPattern).strip()) {
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

    if (password != confirm_password) {
        confirmPasswordError.innerHTML = "Passwords do not match.";
        count++;

    }
    if(count>0){
        return false}
    return true;

}
document.getElementById("searchForm").addEventListener("submit", function(event) {
    let searchInput = document.getElementById("searchInput").value.trim();
    let categorySelect = document.getElementById("categorySelect").value;

    if (searchInput === "" || categorySelect === "") {
        alert("Please enter a search term or select a category.");
        event.preventDefault(); 
    }
});