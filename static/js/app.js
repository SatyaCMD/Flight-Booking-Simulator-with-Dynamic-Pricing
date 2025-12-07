document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const searchBtn = document.querySelector('.search-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    const airportsList = document.getElementById('airports-list');

    if (!document.getElementById('logout-modal')) {
        const modalHtml = `
            <div id="logout-modal" class="modal hidden"
                style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 2000;">
                <div class="glass-panel"
                    style="max-width: 400px; width: 90%; padding: 2rem; text-align: center; background: rgba(17, 34, 64, 0.95); border: 1px solid var(--danger-color);">
                    <div
                        style="width: 60px; height: 60px; background: rgba(239, 68, 68, 0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
                        <i class="fas fa-sign-out-alt" style="font-size: 1.5rem; color: var(--danger-color);"></i>
                    </div>
                    <h3 style="margin-bottom: 1rem; font-size: 1.5rem;">Logout?</h3>
                    <p style="color: var(--text-muted); margin-bottom: 2rem;">Are you sure you want to end your session?</p>
                    <div style="display: flex; gap: 1rem; justify-content: center;">
                        <button id="cancel-logout" class="btn"
                            style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.1);">Cancel</button>
                        <button id="confirm-logout" class="btn"
                            style="background: var(--danger-color); border: none;">Logout</button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const logoutModal = document.getElementById('logout-modal');
        const cancelLogout = document.getElementById('cancel-logout');
        const confirmLogout = document.getElementById('confirm-logout');

        if (cancelLogout) {
            cancelLogout.addEventListener('click', () => {
                logoutModal.classList.add('hidden');
                logoutModal.style.display = 'none';
            });
        }

        if (confirmLogout) {
            confirmLogout.addEventListener('click', () => {
                localStorage.removeItem('user');
                window.location.href = '/';
            });
        }
    }

    if (searchForm) {
        fetchAirports();

        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            searchBtn.disabled = true;
            btnText.textContent = 'Searching...';
            spinner.classList.remove('hidden');
            resultsContainer.innerHTML = '';
            resultsContainer.classList.remove('hidden');

            const formData = new FormData(searchForm);
            const origin = formData.get('origin').toUpperCase();
            const destination = formData.get('destination').toUpperCase();
            const dateRaw = formData.get('date');
            const sortBy = formData.get('sort_by');
            const dateObj = new Date(dateRaw);
            const year = dateObj.getFullYear();
            const month = String(dateObj.getMonth() + 1).padStart(2, '0');
            const day = String(dateObj.getDate()).padStart(2, '0');
            const date = `${year}-${month}-${day}`;

            console.log(`Searching: Origin=${origin}, Destination=${destination}, Date=${date}, Sort=${sortBy}`);

            const searchUrl = `/api/flights/search/?origin=${origin}&destination=${destination}&date=${date}&sort_by=${sortBy}`;
            console.log(`Fetching: ${searchUrl}`);

            try {
                const response = await fetch(searchUrl);
                const flights = await response.json();
                await new Promise(r => setTimeout(r, 600));

                if (flights.length === 0) {
                    resultsContainer.innerHTML = `
                        <div class="glass-panel" style="text-align: center; padding: 3rem;">
                            <i class="fas fa-plane-slash" style="font-size: 3rem; color: #64748b; margin-bottom: 1rem;"></i>
                            <h3>No flights found</h3>
                            <p style="color: #94a3b8;">We couldn't find any flights from <strong>${origin}</strong> to <strong>${destination}</strong> on this date.</p>
                            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">Try checking the available airports in the dropdown.</p>
                        </div>
                    `;
                } else {
                    flights.forEach((flight, index) => {
                        const card = createFlightCard(flight, index);
                        resultsContainer.appendChild(card);
                    });
                }

            } catch (error) {
                console.error('Error:', error);
                resultsContainer.innerHTML = `
                    <div class="glass-panel" style="text-align: center; color: #ef4444;">
                        <p>Something went wrong. Please try again.</p>
                    </div>
                `;
            } finally {
                searchBtn.disabled = false;
                btnText.textContent = 'Search Flights';
                spinner.classList.add('hidden');
            }
        });
    }

    async function fetchAirports() {
        try {
            const response = await fetch('/api/flights/airports/');
            const airports = await response.json();

            if (airportsList) {
                airports.forEach(code => {
                    const option = document.createElement('option');
                    option.value = code;
                    airportsList.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Failed to fetch airports:', error);
        }
    }

    function createFlightCard(flight, index) {
        const div = document.createElement('div');
        div.className = 'flight-card';
        div.style.animationDelay = `${index * 0.1}s`;

        const departure = new Date(flight.departure_time);
        const arrival = new Date(flight.arrival_time);

        const formatTime = (date) => date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const duration = calculateDuration(departure, arrival);
        const price = flight.current_price || flight.base_price;
        const isHighDemand = flight.demand_level > 1.2;
        const isLowSeats = flight.available_seats < 20;

        let badges = '';
        if (isHighDemand) badges += '<span class="badge warning"><i class="fas fa-fire"></i> High Demand</span>';
        if (isLowSeats) badges += '<span class="badge danger"><i class="fas fa-chair"></i> Few Seats</span>';

        div.innerHTML = `
            <div class="airline-logo">${flight.airline_code}</div>
            <div class="route-info">
                <div class="time-row">
                    <span class="time">${formatTime(departure)}</span>
                    <div class="duration-line">
                        <i class="fas fa-plane"></i>
                    </div>
                    <span class="time">${formatTime(arrival)}</span>
                </div>
                <div class="flight-details-row">
                    <span>${flight.origin}</span>
                    <span>${duration}</span>
                    <span>${flight.destination}</span>
                </div>
                <div class="badges-row" style="margin-top: 0.5rem; display: flex; gap: 0.5rem; font-size: 0.8rem;">
                    ${badges}
                </div>
            </div>
            <div class="price-section">
                <span class="price-label">Economy from</span>
                <span class="price">$${price}</span>
                <button class="book-btn" onclick="handleBooking('${flight.flight_id}')">Select</button>
            </div>
        `;
        return div;
    }

    window.handleBooking = function (flightId) {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
            alert('Please login to book a flight.');
            window.location.href = '/login/';
            return;
        }
        window.location.href = `/book/${flightId}/`;
    };

    function calculateDuration(start, end) {
        const diff = end - start;
        const hours = Math.floor(diff / 3600000);
        const minutes = Math.floor((diff % 3600000) / 60000);
        return `${hours}h ${minutes}m`;
    }
    checkAuthStatus();
});

function checkAuthStatus() {
    console.log("Checking Auth Status...");
    const userStr = localStorage.getItem('user');
    const loginBtn = document.querySelector('.login-btn');
    const profileLink = document.querySelector('.profile-link');

    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            console.log("User logged in:", user.email);

            if (loginBtn) {
                loginBtn.textContent = 'Logout';
                loginBtn.href = '#';
                loginBtn.classList.add('logout-btn');
                const newLoginBtn = loginBtn.cloneNode(true);
                loginBtn.parentNode.replaceChild(newLoginBtn, loginBtn);
                newLoginBtn.addEventListener('click', (e) => {
                    e.preventDefault();

                    const logoutModal = document.getElementById('logout-modal');
                    if (logoutModal) {
                        logoutModal.classList.remove('hidden');
                        logoutModal.style.display = 'flex';
                    } else {
                        // Fallback (should not happen if injection works)
                        if (confirm('Are you sure you want to logout?')) {
                            localStorage.removeItem('user');
                            window.location.href = '/login/';
                        }
                    }
                });
            }

            if (profileLink) {
                profileLink.classList.remove('hidden');

                let memIdDisplay = document.getElementById('nav-membership-id');
                if (!memIdDisplay) {
                    memIdDisplay = document.createElement('span');
                    memIdDisplay.id = 'nav-membership-id';
                    memIdDisplay.style.color = '#fbbf24'; // Gold color
                    memIdDisplay.style.fontWeight = '600';
                    memIdDisplay.style.marginRight = '1.5rem';
                    memIdDisplay.style.fontSize = '0.9rem';
                    memIdDisplay.style.display = 'inline-flex';
                    memIdDisplay.style.alignItems = 'center';
                    memIdDisplay.innerHTML = `<i class="fas fa-crown" style="margin-right: 0.5rem;"></i> ${user.membership_id || 'Member'}`;

                    const navLinks = document.querySelector('.nav-links');
                    if (navLinks) {
                        navLinks.insertBefore(memIdDisplay, document.querySelector('.login-btn'));
                    }
                }
            }
        } catch (e) {
            console.error("Error parsing user data:", e);
            localStorage.removeItem('user'); // Clear invalid data
        }
    } else {
        console.log("No user logged in.");
        if (profileLink) {
            profileLink.classList.add('hidden');
        }

        const memIdDisplay = document.getElementById('nav-membership-id');
        if (memIdDisplay) {
            memIdDisplay.remove();
        }

        if (loginBtn) {
            loginBtn.textContent = 'Login';
            loginBtn.href = '/login/';
            loginBtn.classList.remove('logout-btn');
            const newLoginBtn = loginBtn.cloneNode(true);
            loginBtn.parentNode.replaceChild(newLoginBtn, loginBtn);
        }
    }
}
