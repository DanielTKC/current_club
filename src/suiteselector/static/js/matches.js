/*!
* Author: Daniel Terreros
* This is the script that pulls down available matches, checks to see if user is logged in if they try to book
* Sends an alert and sends them to the login page.
*/

document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const suiteId = urlParams.get('suiteId');

    if (suiteId) {
        // Fetch and display suites available for the selected match
        fetchAvailableMatchesForSuite(suiteId);
    } else {
        // Fetch and display all suites
        fetchAllMatches();
    }
});

function fetchAvailableMatchesForSuite(suiteId) {
    fetch(`/api/suites/${suiteId}/`)
        .then(response => response.json())
        .then(data => {
            const matches = data.available_matches;
            displayMatches(matches);
        })
        .catch(error => console.error('Error:', error));
}

function fetchAllMatches() {
    fetch(`/api/matches/`)
        .then(response => response.json())
        .then(matches => {
            displayMatches(matches);
        })
        .catch(error => console.error('Error:', error));
}

function displayMatches(matches) {
    console.log("We're displaying matches")
}

function bookNow(matchId, suiteId) {
    // Check if the user is authenticated
    fetch('/api/check-auth/')
        .then(response => {
            if (response.ok) {
                // User is authenticated, proceed to reservation form
                window.location.href = `/reservation/${matchId}/${suiteId}/`;
            } else {
                // User is not authenticated, redirect to login page
                window.location.href = `/login/?next=/reservation/${matchId}/${suiteId}/`;
            }
        });
}
//console.log('matches.js loaded');
function viewOptions(matchId) {
    window.location.href = `/suites/?matchId=${matchId}`;
  // fetch(`/api/matches/${matchId}/`)
  // .then(response => response.json())
  // .then(data => {
  //     const container = document.getElementById('suiteAvailabilityContainer');
  //     // Clear previous content
  //     container.innerHTML = '';
  //
  //     // Create the initial section and row structure
  //     const section = document.createElement('section');
  //     section.className = 'py-5 bg-white';
  //
  //     const divContainer = document.createElement('div');
  //     divContainer.className = 'container px-4 mt-5';
  //
  //     const row = document.createElement('div');
  //     row.className = 'row gx-4 gx-lg-5  justify-content-center';
  //
  //
  //     // Append everything
  //     divContainer.appendChild(row);
  //     section.appendChild(divContainer);
  //     container.appendChild(section);
  //
  //     // Now loop through data
  //     data.available_suites.forEach(suite => {
  //       const suiteElement = document.createElement('div');
  //
  //       suiteElement.className = 'col-12 mb-5';
  //       suiteElement.innerHTML = `
  //           <div class ="card text-center">
  //           <div class="card high-card">
  //               <!-- Suite details here -->
  //               <h5 class="card-header">${suite.name}</h5>
  //               <div class="card-body">
  //
  //
  //                   <p class="card-text">Seat Capacity: ${suite.capacity}</p>
  //                   <p class="card-text">Price: $${(suite.price * suite.capacity).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
  //
  //               </div>
  //               <div class="card-footer">
  //                   <button class="btn btn-primary book-suite-btn">Book Suite</button>
  //               </div>
  //           </div>
  //           </div>
  //       `;
  //
  //         row.appendChild(suiteElement);
  //
  //     });
  //
  //     attachBookSuiteEventListeners();
  //
  //
  //
  //     if (data.length === 0) {
  //         row.innerHTML = '<p>No available suites for this match.</p>';
  //     }
  // })
  // .catch(error => console.error('Error:', error));
}

// function attachBookSuiteEventListeners() {
//   //console.log('Attaching event listeners...');
//   document.querySelectorAll('.book-suite-btn').forEach(button => {
//       // clear previous handlers
//       //console.log('Button found', button);
//       button.removeEventListener('click', bookSuiteHandler);
//       // add new handler
//       button.addEventListener('click', bookSuiteHandler);
//   });
// }
//
// function bookSuiteHandler() {
//     // Make an asynchronous request to check the authentication status
//     fetch('/api/check-auth/')
//       .then(response => {
//         if (response.ok) {
//           // If the response is OK, the user is logged in
//           console.log('Booking suite...');
//           // You can proceed with booking the suite here
//         } else {
//           // If the response is not OK, the user is not logged in
//           alert('Please log in or create an account to book a suite.');
//           window.location.href = '/registration';
//         }
//       })
//       .catch(error => {
//         console.error('Error:', error);
//       });
//   }
  
