function logout() {
    localStorage.removeItem('email');

}

setTimeout(function() {
    var categoryErrorAlert = document.getElementById('alert-category-error');
    if (categoryErrorAlert) {
        categoryErrorAlert.parentNode.removeChild(categoryErrorAlert);
    }

    var alertMessages = document.querySelectorAll('.alert');
    alertMessages.forEach(function(alert) {
        alert.parentNode.removeChild(alert);
    });
}, 2500);
