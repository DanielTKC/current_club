document.addEventListener("DOMContentLoaded", function() {
  // Check if the token exists in localStorage
  const token = localStorage.getItem("token");
  
  if (token) {
    // User is logged in, change the UI accordingly
    document.getElementById("loginButton").style.display = "none"; // Hide login button
    const userDropdown = document.getElementById("userDropdown");
    userDropdown.style.display = "block"; // Show user dropdown
    // Set the username 
    // userDropdown.textContent = `Logged in as ${username}`;
  } else {
    // User is not logged in, show login button
    document.getElementById("loginButton").style.display = "block";
    document.getElementById("userDropdown").style.display = "none";
  }
});

document.getElementById('logoutLink').addEventListener('click', function() {
  fetch('/api/logout/', {
    //console.log("we're logging out");
      method: 'GET', 
      credentials: 'include' // CRSF
  })
  .then(response => {
      if(response.ok) {
          
          localStorage.removeItem('token'); 
          window.location.href = '/'; 
      }
  })
  .catch(error => console.error('Error:', error));
});