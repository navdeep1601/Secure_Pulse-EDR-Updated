// Configuration: Point this to your Flask server
const API_URL = 'http://127.0.0.1:5000/events';
let lastEventId = 0;

/**
 * Fetches the latest intrusion events from the SecurePulse backend
 */
async function fetchIntrusions() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const events = await response.json();
        updateTable(events);
    } catch (error) {
        console.error('Error fetching data from SecurePulse API:', error);
    }
}

/**
 * Dynamically updates the HTML table with event data
 */
function updateTable(events) {
    const tableBody = document.getElementById('eventBody');
    
    // We reverse the events to show the newest ones at the top
    const latestEvents = events.reverse();

    // Clear existing rows to prevent duplicates
    tableBody.innerHTML = '';

    latestEvents.forEach(event => {
        const row = document.createElement('tr');
        
        // If this is a brand new event, give it a CSS class for a "flash" effect
        if (event.id > lastEventId && lastEventId !== 0) {
            row.classList.add('new-alert');
        }

        row.innerHTML = `
            <td>${event.timestamp}</td>
            <td><strong>${event.attacker_ip}</strong></td>
            <td><span class="port-badge">${event.port}</span></td>
            <td>${event.service}</td>
            <td class="payload-text">${event.payload || 'Scanning Activity'}</td>
        `;
        
        tableBody.appendChild(row);
    });

    // Update the last known ID for the next refresh cycle
    if (events.length > 0) {
        lastEventId = Math.max(...events.map(e => e.id));
    }
}

// Initial fetch when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log("[*] Mirage Dashboard Connected.");
    fetchIntrusions();
    
    // Refresh every 2 seconds (Real-time feel)
    setInterval(fetchIntrusions, 2000);
});