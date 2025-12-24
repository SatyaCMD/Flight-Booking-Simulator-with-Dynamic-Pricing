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
            <div class="airline-logo" style="color: black !important;">${flight.airline_code}</div>
            <div class="route-info" style="color: black !important;">
                <div class="time-row">
                    <span class="time" style="color: black !important; font-weight: 700;">${formatTime(departure)}</span>
                    <div class="duration-line">
                        <i class="fas fa-plane"></i>
                    </div>
                    <span class="time" style="color: black !important; font-weight: 700;">${formatTime(arrival)}</span>
                </div>
                <div class="flight-details-row">
                    <span style="color: black !important; font-weight: 600;">${flight.origin}</span>
                    <span style="color: black !important;">${duration}</span>
                    <span style="color: black !important; font-weight: 600;">${flight.destination}</span>
                </div>
                <div class="badges-row" style="margin-top: 0.5rem; display: flex; gap: 0.5rem; font-size: 0.8rem;">
                    ${badges}
                </div>
            </div>
            <div class="price-section" style="color: black !important;">
                <span class="price-label" style="color: black !important;">Economy from</span>
                <span class="price" style="color: black !important;">$${price}</span>
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
                    e.stopPropagation();

                    if (!document.getElementById('logout-modal')) {
                        const modalHtml = `
                            <div id="logout-modal" class="modal hidden"
                                style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 2000; opacity: 0; transition: opacity 0.3s ease;">
                                <div class="glass-panel"
                                    style="max-width: 400px; width: 90%; padding: 2.5rem; text-align: center; background: white; border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); transform: scale(0.9); transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);">
                                    <div
                                        style="width: 80px; height: 80px; background: #FEF2F2; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; border: 2px solid #FECACA; box-shadow: 0 4px 6px -1px rgba(185, 28, 28, 0.1);">
                                        <i class="fas fa-plane-departure" style="font-size: 2rem; color: #B91C1C; transform: rotate(-45deg);"></i>
                                    </div>
                                    <h3 style="margin-bottom: 0.5rem; font-size: 1.8rem; font-family: 'Playfair Display', serif; font-weight: 700; color: #1E293B;">Leaving so soon?</h3>
                                    <p style="color: #64748b; margin-bottom: 2rem; font-family: 'Outfit', sans-serif; font-size: 1.1rem;">Ready to disembark from your session?</p>
                                    <div style="display: flex; gap: 1rem; justify-content: center;">
                                        <button id="cancel-logout"
                                            style="padding: 0.75rem 2rem; border-radius: 50px; border: 2px solid #e2e8f0; background: white; color: #64748b; font-weight: 600; cursor: pointer; transition: all 0.2s; font-family: 'Outfit', sans-serif;">Stay Onboard</button>
                                        <button id="confirm-logout"
                                            style="padding: 0.75rem 2rem; border-radius: 50px; border: none; background: linear-gradient(135deg, #B91C1C 0%, #991B1B 100%); color: white; font-weight: 600; cursor: pointer; box-shadow: 0 4px 15px -3px rgba(185, 28, 28, 0.4); transition: all 0.2s; font-family: 'Outfit', sans-serif;">Sign Out</button>
                                    </div>
                                </div>
                            </div>
                        `;
                        document.body.insertAdjacentHTML('beforeend', modalHtml);

                        const modal = document.getElementById('logout-modal');
                        const panel = modal.querySelector('.glass-panel');
                        const cancelBtn = document.getElementById('cancel-logout');
                        const confirmBtn = document.getElementById('confirm-logout');

                        cancelBtn.onmouseover = () => { cancelBtn.style.background = '#f8fafc'; cancelBtn.style.borderColor = '#cbd5e1'; };
                        cancelBtn.onmouseout = () => { cancelBtn.style.background = 'white'; cancelBtn.style.borderColor = '#e2e8f0'; };

                        confirmBtn.onmouseover = () => { confirmBtn.style.transform = 'translateY(-2px)'; confirmBtn.style.boxShadow = '0 10px 20px -5px rgba(185, 28, 28, 0.5)'; };
                        confirmBtn.onmouseout = () => { confirmBtn.style.transform = 'translateY(0)'; confirmBtn.style.boxShadow = '0 4px 15px -3px rgba(185, 28, 28, 0.4)'; };

                        cancelBtn.addEventListener('click', () => {
                            modal.style.opacity = '0';
                            panel.style.transform = 'scale(0.9)';
                            setTimeout(() => {
                                modal.classList.add('hidden');
                                modal.style.display = 'none';
                            }, 300);
                        });

                        confirmBtn.addEventListener('click', () => {
                            localStorage.removeItem('user');
                            window.location.href = '/login/';
                        });
                    }

                    const logoutModal = document.getElementById('logout-modal');
                    const panel = logoutModal.querySelector('.glass-panel');

                    if (!logoutModal.dataset.listenersAttached) {
                        const cancelBtn = document.getElementById('cancel-logout');
                        const confirmBtn = document.getElementById('confirm-logout');

                        if (cancelBtn && confirmBtn) {
                            cancelBtn.addEventListener('click', () => {
                                logoutModal.style.opacity = '0';
                                panel.style.transform = 'scale(0.9)';
                                setTimeout(() => {
                                    logoutModal.classList.add('hidden');
                                    logoutModal.style.display = 'none';
                                }, 300);
                            });

                            confirmBtn.addEventListener('click', () => {
                                localStorage.removeItem('user');
                                window.location.href = '/login/';
                            });
                            logoutModal.dataset.listenersAttached = 'true';
                        }
                    }

                    logoutModal.classList.remove('hidden');
                    logoutModal.style.display = 'flex';

                    requestAnimationFrame(() => {
                        logoutModal.style.opacity = '1';
                        panel.style.transform = 'scale(1)';
                    });
                });
                let memIdDisplay = document.getElementById('nav-membership-id');
                if (!memIdDisplay) {
                    memIdDisplay = document.createElement('span');
                    memIdDisplay.id = 'nav-membership-id';
                    memIdDisplay.style.color = '#fbbf24'; 
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
            localStorage.removeItem('user'); 
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
