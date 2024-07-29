// ==UserScript==
// @name        Response Time V2
// @namespace   Violentmonkey Scripts
// @match       https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx*
// @grant       none
// @version     1.0
// @author      Gavin Olson
// @description 7/26/2024, 1:11:37 PM
// ==/UserScript==


(function() {
    'use strict';

    // Hardcoded URL
    const MEETING_URL = 'https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2704';

    // Variables to be set by user
    let DURATION_MINUTES, TIME_LINE, PAUSE_TIME;
    let timestamps = [];
    let loadTimes = [];

    function createUI() {
        const uiContainer = document.createElement('div');
        uiContainer.id = 'load-times-ui';
        uiContainer.style.position = 'fixed';
        uiContainer.style.bottom = '10px'; // Position at the top
        uiContainer.style.right = '10px'; // Position at the right
        uiContainer.style.backgroundColor = 'white';
        uiContainer.style.border = '1px solid black';
        uiContainer.style.padding = '15px';
        uiContainer.style.zIndex = '1000';
        uiContainer.style.maxWidth = '600px';
        uiContainer.style.maxHeight = '600px';
        uiContainer.style.overflow = 'auto';
        uiContainer.style.fontFamily = 'Arial, sans-serif';
        uiContainer.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.2)';

        uiContainer.innerHTML = `
            <h3>Load Times</h3>
            <div id="input-form">
                <label for="duration">Duration (minutes):</label>
                <input type="number" id="duration" min="1" step="0.1" required><br>
                <label for="time-line">Expected Response Time (Seconds):</label>
                <input type="number" id="time-line" min="1" step="1" required><br>
                <label for="pause-time">Pause Time (seconds):</label>
                <input type="number" id="pause-time" min="1" step="1" required><br>
                <button id="start-btn" style="margin-top: 10px;">Start</button>
            </div>
            <div id="data-container" style="display: none;">
                <p>Collecting data...</p>
            </div>
            <button id="download-btn" style="margin-top: 10px;" disabled>Download Data</button>
            <button id="show-stats-btn" style="margin-top: 10px;" disabled>Show Statistics</button>
        `;
        document.body.appendChild(uiContainer);

        document.getElementById('start-btn').addEventListener('click', () => {
            DURATION_MINUTES = parseFloat(document.getElementById('duration').value);
            TIME_LINE = parseInt(document.getElementById('time-line').value, 10) * 1000;
            PAUSE_TIME = parseInt(document.getElementById('pause-time').value, 10);

            if (isNaN(DURATION_MINUTES) || isNaN(TIME_LINE) || isNaN(PAUSE_TIME)) {
                alert("Please enter valid values.");
                return;
            }

            document.getElementById('input-form').style.display = 'none';
            document.getElementById('data-container').style.display = 'block';
            collectLoadTimes();
        });

        document.getElementById('download-btn').addEventListener('click', () => {
            const data = formatData(timestamps, loadTimes);
            generateDownloadLink(data, `LoadTimes_${new Date().toISOString()}.txt`);
        });

        document.getElementById('show-stats-btn').addEventListener('click', () => {
            const stats = calculateStatistics(loadTimes);
            showStatistics(stats);
            // Disable the button after clicking
            document.getElementById('show-stats-btn').disabled = true;
        });
    }

    function updateUI(requestNumber, loadTime) {
    const dataContainer = document.getElementById('data-container');
    const responseTime = TIME_LINE / 1000; // Convert TIME_LINE from milliseconds to seconds
    const doubleResponseTime = responseTime * 2; // Twice the expected response time

    let color;
    if (loadTime < responseTime) {
        color = 'green'; // Below expected response time
    } else if (loadTime < doubleResponseTime) {
        color = '#FFC107'; // Between expected response time and twice the expected response time
    } else {
        color = 'red'; // More than twice the expected response time
      }

    dataContainer.innerHTML = `
        <p><strong>Request #${requestNumber}</strong></p>
        <p><strong>Load Time:</strong> <span style="color: ${color};">${loadTime} seconds</span></p>
    `;
    }

    function showStatistics(stats) {
        const dataContainer = document.getElementById('data-container');
        dataContainer.innerHTML += `
            <h4>Statistics:</h4>
            <p>Counts Exceeding Expected Response Time (${TIME_LINE / 1000} seconds): ${stats.countExceeding}</p>
            <p>Mean: ${stats.mean.toFixed(2)} seconds</p>
            <p>Median: ${stats.median.toFixed(2)} seconds</p>
            <p>Max: ${stats.max.toFixed(2)} seconds</p>
            <p>Min: ${stats.min.toFixed(2)} seconds</p>
        `;
    }

    async function fetchPage(url) {
        try {
            const start = performance.now(); // Start timing in milliseconds
            await fetch(url); // Make a request to the URL
            const end = performance.now(); // End timing in milliseconds
            const loadTime = end - start; // Load time in milliseconds
            return loadTime / 1000; // Convert load time to seconds
        } catch (error) {
            console.error('Error fetching page:', error);
            return null;
        }
    }

    async function collectLoadTimes() {
        const endTime = Date.now() + DURATION_MINUTES * 60 * 1000;
        let requestNumber = 0;

        while (Date.now() < endTime) {
            const timestamp = new Date().toISOString();
            const loadTime = await fetchPage(MEETING_URL);

            if (loadTime !== null) {
                console.log(`Timestamp: ${timestamp}, Raw Load Time: ${loadTime * 1000} ms, Converted Load Time: ${loadTime.toFixed(2)} seconds`);

                if (loadTime < TIME_LINE / 1000) {
                    await new Promise(resolve => setTimeout(resolve, 5000)); // Pause for 5 seconds
                } else {
                    await new Promise(resolve => setTimeout(resolve, PAUSE_TIME * 1000)); // Pause for PAUSE_TIME seconds
                }

                timestamps.push(timestamp);
                loadTimes.push(loadTime.toFixed(2)); // Store in seconds

                // Update the UI with the latest data
                updateUI(++requestNumber, loadTime.toFixed(2));
            }
        }

        // After data collection is complete, enable the buttons
        const dataContainer = document.getElementById('data-container');
        dataContainer.innerHTML += '<p>Data collection completed. You can now download the data or view statistics.</p>';
        document.getElementById('download-btn').disabled = false;
        document.getElementById('show-stats-btn').disabled = false;
    }

    function generateDownloadLink(data, filename) {
        const blob = new Blob([data], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function formatData(timestamps, loadTimes) {
        let data = "Timestamp and Loading Times:\n";
        data += "----------------------------\n";
        for (let i = 0; i < timestamps.length; i++) {
            data += `${timestamps[i]}\t${loadTimes[i]} seconds\n`;
        }
        data += "----------------------------\n";
        return data;
    }

    function calculateStatistics(loadTimes) {
        const times = loadTimes.map(Number);
        const countExceeding = times.filter(time => time > TIME_LINE / 1000).length;
        const mean = times.reduce((a, b) => a + b, 0) / times.length;
        const median = times.sort((a, b) => a - b)[Math.floor(times.length / 2)];
        const max = Math.max(...times);
        const min = Math.min(...times);

        return {
            countExceeding,
            mean,
            median,
            max,
            min
        };
    }

    // Initialize the UI
    createUI();
})();