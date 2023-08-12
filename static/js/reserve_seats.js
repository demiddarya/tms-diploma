document.addEventListener('DOMContentLoaded', function () {
    const reserveButton = document.getElementById('reserve-seats-button');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const checkedSeats = Array.from(checkboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.id.split(" ")[1]);

            reserveButton.disabled = checkedSeats.length <= 0;
        });
    });

    function updateReserveButtonState() {
        const checkedSeats = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.id.split(" ")[1]);

        reserveButton.disabled = checkedSeats.length === 0;
    }

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            updateReserveButtonState();
        });
    });

    updateReserveButtonState();

    function fetchPurchasedTickets() {
        const screeningId = window.location.pathname.split('/').pop();

        fetch(`/api/purchased_tickets/${screeningId}`)
            .then(response => response.json())
            .then(data => {
                const purchasedSeats = data.map(ticket => ticket.seat_number);

                checkboxes.forEach(checkbox => {
                    const seatNumber = Number(checkbox.id.split(" ")[1]);
                    checkbox.disabled = purchasedSeats.includes(seatNumber);
                });
            })
            .catch(error => {
                console.error('Error fetching purchased tickets:', error);
            });
    }
    fetchPurchasedTickets();

    reserveButton.addEventListener('click', function () {
        const checkedSeats = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.id.split(" ")[1]);

        console.log('Seats: ' + checkedSeats);
        if (checkedSeats.length > 0) {
            const urlParams = new URLSearchParams();
            urlParams.append('seats', checkedSeats.join(','));

            const screeningId = window.location.pathname.split('/').pop();
            urlParams.append('screening_id', screeningId);

            const reserveURL = 'reserve_seats' + '?' + urlParams.toString();
            window.location.href = reserveURL;
        } else {
            alert('Choose one or more seats!');
        }
    });
});
