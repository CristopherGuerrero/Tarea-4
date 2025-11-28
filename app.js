document.getElementById("loginForm").addEventListener("submit", function(event){
    event.preventDefault();

    const user = document.getElementById("username").value.trim();
    const pass = document.getElementById("password").value.trim();
    const error = document.getElementById("loginError");

    // Validación: campos vacíos
    if(user === "" || pass === "") {
        error.textContent = "Los campos no pueden estar vacíos";
        return;
    }

    // Validación: usuario muy corto
    if(user.length < 3) {
        error.textContent = "El usuario es muy corto";
        return;
    }

    // Validación: contraseña demasiado larga
    if(pass.length > 20) {
        error.textContent = "La contraseña es demasiado larga";
        return;
    }

    // Validación de credenciales
    if(user === "admin" && pass === "1234") {
        window.location.href = "dashboard.html";
    } else {
        error.textContent = "Credenciales incorrectas";
    }
});
