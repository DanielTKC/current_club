(function () {
    'use strict'
    const forms = document.querySelectorAll('.requires-validation')
    Array.from(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

document.getElementById('registrationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    fetch('/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(registrationData => {
        if (registrationData.error) {
            throw new Error('Registration failed: ' + registrationData.error);
        }
        console.log('Registration Success:', registrationData);

        const loginData = { username: data.email, password: data.password, first_name: data.first_name, last_name: data.last_name, 
            address: data.address, city: data.city, state: data.state, zip_code: data.zip_code, phone_number: data.phone_number };


        return fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(loginData),
        });
    })
    .then(response => response.json())
    .then(loginData => {
        if (loginData.error) {
            throw new Error('Login failed: ' + loginData.error);
        }
        console.log('Login Success:', loginData);
        localStorage.setItem('authToken', loginData.token);
        // Redirect after successful login
        window.location.href = '/matches';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
