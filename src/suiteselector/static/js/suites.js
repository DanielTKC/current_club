document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const matchId = urlParams.get('matchId');

    if (matchId) {
        // Fetch and display suites available for the selected match
        fetchAvailableSuitesForMatch(matchId);
    } else {
        // Fetch and display all suites
        fetchAllSuites();
    }
});

function fetchAvailableSuitesForMatch(matchId) {
    fetch(`/api/matches/${matchId}/`)
        .then(response => response.json())
        .then(data => {
            const suites = data.available_suites;
            displaySuites(suites);
        })
        .catch(error => console.error('Error:', error));
}

function fetchAllSuites() {
    fetch(`/api/suites/`)
        .then(response => response.json())
        .then(suites => {
            displaySuites(suites);
        })
        .catch(error => console.error('Error:', error));
}

function displaySuites(suites) {
    console.log("We're displaying suites")
}


function viewOptions(suiteId) {
    window.location.href = `/matches/?suiteId=${suiteId}`;
}

function bookNow(matchId, suiteId) {
    // Check if the user is authenticated
    console.log("booknow clicked")
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

