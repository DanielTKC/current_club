    function cancelReservation(reservationId) {
        fetch(`/api/reservations/${reservationId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (response.ok) {
                // Reservation canceled successfully
                window.location.reload();
            } else {
                // Handle cancellation failure
                console.error('Failed to cancel reservation');
            }
        })
        .catch(error => {
            console.error('Error canceling reservation:', error);
        });
    }