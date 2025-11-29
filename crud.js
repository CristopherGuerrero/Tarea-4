let records = JSON.parse(localStorage.getItem("users")) || [];

function renderTable() {
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = "";

    records.forEach((rec, index) => {
        tbody.innerHTML += `
            <tr>
                <td>${rec.name}</td>
                <td>${rec.email}</td>
                <td>${rec.age}</td>
                <td>
                    <button onclick="editRecord(${index})">Editar</button>
                    <button onclick="deleteRecord(${index})">Eliminar</button>
                </td>
            </tr>
        `;
    });
}

function addRecord() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const age = parseInt(document.getElementById("age").value.trim());
    const index = document.getElementById("editIndex").value;


    if(name === "" || email === "" || isNaN(age)) {
        alert("Todos los campos son obligatorios");
        return;
    }

    if(name.length > 50) {
        alert("El nombre es demasiado largo");
        return;
    }

    if(!email.includes("@") || !email.includes(".")) {
        alert("El correo no es válido");
        return;
    }

    if(age <= 0) {
        alert("La edad debe ser mayor que 0");
        return;
    }

    if(age > 120) {
        alert("La edad no puede superar los 120 años");
        return;
    }


    if(index === "") { 
        records.push({name, email, age});
    } else {
        records[index] = {name, email, age};
        document.getElementById("editIndex").value = "";
    }

    localStorage.setItem("users", JSON.stringify(records));
    renderTable();

    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("age").value = "";
}

function editRecord(index) {
    const rec = records[index];

    document.getElementById("name").value = rec.name;
    document.getElementById("email").value = rec.email;
    document.getElementById("age").value = rec.age;

    document.getElementById("editIndex").value = index;
}

function deleteRecord(index) {
    records.splice(index, 1);
    localStorage.setItem("users", JSON.stringify(records));
    renderTable();
}

renderTable();
