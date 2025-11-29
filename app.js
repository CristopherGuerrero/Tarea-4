document.getElementById("loginForm").addEventListener("submit", function(event){
    event.preventDefault();

    const user = document.getElementById("username").value.trim();
    const pass = document.getElementById("password").value.trim();
    const error = document.getElementById("loginError");

    if(user === "" || pass === "") {
        error.textContent = "Los campos no pueden estar vacíos";
        return;
    }

    if(user.length < 3) {
        error.textContent = "El usuario es muy corto";
        return;
    }

    if(pass.length > 20) {
        error.textContent = "La contraseña es demasiado larga";
        return;
    }

    if(user === "admin" && pass === "1234") {
        window.location.href = "dashboard.html";
    } else {
        error.textContent = "Credenciales incorrectas";
    }
});
