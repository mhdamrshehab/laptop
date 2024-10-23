// Once the user logout , the email in the local storage will be removed
function logout() {
    localStorage.removeItem('email');

}

// setTimeout to remove the alert message that diplay the flash comes for the flask return 
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

// Theme Mode functions
function applyTheme(theme) {
    if (theme === 'dark') {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }

  function saveTheme(theme) {
    localStorage.setItem('theme', theme);
  }
  const savedTheme = localStorage.getItem('theme');

  if (savedTheme) {
    applyTheme(savedTheme);
  } else {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(systemPrefersDark ? 'dark' : 'light');
  }
  // Select the brower theme mode and apply it on the project.
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    const newTheme = event.matches ? 'dark' : 'light';
    applyTheme(newTheme);
    saveTheme(newTheme);
  });
  
  document.getElementById('theme').addEventListener('click', function () {
    const currentTheme = document.body.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    saveTheme(newTheme);
  });