document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const data = Object.fromEntries(formData.entries());

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch('/api/login/', {  
    // console.log("WE"RE FETCHING BOYS!")
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({username: data.username, password: data.password}),
  })
  .then(response => response.json())  // Parse JSON response
  .then(data => {
      console.log('Login success:', data);
      localStorage.setItem('token', data.token); // Store the token
      window.location.href = '/';  // Redirect user
  })
  .catch((error) => {
      console.error('Error:', error);
  });
});
