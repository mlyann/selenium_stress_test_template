// ==UserScript==
// @name        Response Time V2
// @namespace   Violentmonkey Scripts
// @match       https://blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx*
// @grant       none
// @version     1.9
// @author      Gavin Olson
// @description 8/2/2024, 3:00:00 PM
// ==/UserScript==

(function() {
    'use strict';

    // Hardcoded URL
    const MEETING_URL = window.location.href;

    // Variables to be set by user
    let DURATION_MINUTES, TIME_LINE, PAUSE_TIME;
    let timestamps = [];
    let loadTimes = [];
    let startTime; // To keep track of when the collection starts
    let chart; // Chart.js instance
    let isGraphInitialized = false; // Track if the graph has been initialized

    function loadChartJs(callback) {
        // Load Chart.js library
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        document.head.appendChild(script);
        script.onload = () => {
            // Load Chart.js plugin annotation
            const pluginScript = document.createElement('script');
            pluginScript.src = 'https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation';
            document.head.appendChild(pluginScript);
            pluginScript.onload = callback; // Call the callback function once the plugin is loaded
        };
    }

    function createUI() {
        const uiContainer = document.createElement('div');
        uiContainer.id = 'load-times-ui';
        uiContainer.style.position = 'fixed';
        uiContainer.style.bottom = '10px'; // Position at the bottom
        uiContainer.style.right = '10px'; // Position at the right
        uiContainer.style.backgroundColor = 'white';
        uiContainer.style.border = '1px solid black';
        uiContainer.style.padding = '10px'; // Reduced padding initially
        uiContainer.style.zIndex = '1000';
        uiContainer.style.maxWidth = '500px'; // Reduced width initially
        uiContainer.style.maxHeight = '300px'; // Reduced height initially
        uiContainer.style.overflow = 'auto';
        uiContainer.style.fontFamily = 'Arial, sans-serif';
        uiContainer.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.2)';

        uiContainer.innerHTML = `
            <h3>Load Times</h3>
            <div id="input-form">
                <label for="duration">Duration (minutes):</label>
                <input type="number" id="duration" min="1" step="0.1" required><br>
                <label for="time-line">Expected Response Time (Seconds):</label>
                <input type="number" id="time-line" min="0.1" step="0.1" required><br>
                <label for="pause-time">Pause Time (seconds):</label>
                <input type="number" id="pause-time" min="0.1" step="0.1" required><br>
                <button id="start-btn" style="margin-top: 10px;">Start</button>
            </div>
            <div id="data-container" style="display: none;">
                <p>Collecting data...</p>
            </div>
            <button id="download-btn" style="margin-top: 10px;" disabled>Download Data</button>
            <button id="show-stats-btn" style="margin-top: 10px;" disabled>Show Statistics</button>
            <button id="download-graph-btn" style="margin-top: 10px; display: none;">Download Graph</button>
            <div id="chart-container" style="display: none; margin-top: 20px;">
                <h4>Load Time Chart</h4>
                <canvas id="load-times-chart" width="300" height="200"></canvas> <!-- Reduced canvas size initially -->
            </div>
        `;
        document.body.appendChild(uiContainer);

        document.getElementById('start-btn').addEventListener('click', () => {
            DURATION_MINUTES = parseFloat(document.getElementById('duration').value);
            TIME_LINE = parseFloat(document.getElementById('time-line').value, 10) * 1000;
            PAUSE_TIME = parseFloat(document.getElementById('pause-time').value, 10);

            if (isNaN(DURATION_MINUTES) || isNaN(TIME_LINE) || isNaN(PAUSE_TIME)) {
                alert("Please enter valid values.");
                return;
            }

            document.getElementById('input-form').style.display = 'none';
            document.getElementById('data-container').style.display = 'block';
            document.getElementById('chart-container').style.display = 'block'; // Show the chart container
            document.getElementById('load-times-chart').width = '600'; // Adjust canvas size for the chart
            document.getElementById('load-times-chart').height = '400';
            uiContainer.style.maxWidth = '600px'; // Expand the UI container width
            uiContainer.style.maxHeight = '600px'; // Expand the UI container height
            uiContainer.style.padding = '15px'; // Expand the padding

            startTime = Date.now(); // Record start time

            // Initialize chart here
            loadChartJs(() => {
                createChart(); // Create the chart
                collectLoadTimes(); // Start data collection
            });
        });

        document.getElementById('download-btn').addEventListener('click', () => {
            const data = formatData(timestamps, loadTimes);
            generateDownloadLink(data, `LoadTimes_${new Date().toISOString()}.csv`);
        });

        document.getElementById('show-stats-btn').addEventListener('click', () => {
            const stats = calculateStatistics(loadTimes);
            showStatistics(stats);
            // Disable the button after clicking
            document.getElementById('show-stats-btn').disabled = true;
        });

        document.getElementById('download-graph-btn').addEventListener('click', () => {
            downloadGraph();
        });
    }

    function updateUI(requestNumber, loadTime) {
        const dataContainer = document.getElementById('data-container');
        const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000); // Calculate elapsed time in seconds
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
            <p><strong>Request #${requestNumber} - ${elapsedSeconds} seconds elapsed</strong></p>
            <p><strong>Load Time:</strong> <span style="color: ${color};">${loadTime} seconds</span></p>
        `;

        // Update chart if it's visible
        if (chart) {
            chart.data.labels.push(`${elapsedSeconds}s`);
            chart.data.datasets[0].data.push(loadTime);
            adjustYAxis();
            chart.update();
        }
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

    function createChart() {
        const ctx = document.getElementById('load-times-chart').getContext('2d');

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: timestamps.map((_, index) => `${index + 1}`),
                datasets: [{
                    label: 'Load Time (seconds)',
                    data: loadTimes.map(time => parseFloat(time)),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Elapsed Time (seconds)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Load Time (Seconds)'
                        },
                        beginAtZero: false
                        // No need to set min/max initially, they will be set dynamically
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            line: {
                                type: 'line',
                                yMin: TIME_LINE / 1000,
                                yMax: TIME_LINE / 1000,
                                borderColor: 'red',
                                borderWidth: 2,
                                borderDash: [10, 5], // Dotted line
                                label: {
                                    content: 'Expected Response Time',
                                    enabled: true,
                                    position: 'top'
                                }
                            }
                        }
                    }
                }
            }
        });

        document.getElementById('download-graph-btn').style.display = 'inline-block'; // Show the download graph button
    }

    function adjustYAxis() {
        if (chart) {
            const allData = chart.data.datasets[0].data;
            const minLoadTime = Math.min(...allData) - 1; // Adjust as needed
            const maxLoadTime = Math.max(...allData) + 1; // Adjust as needed
            chart.options.scales.y.min = minLoadTime;
            chart.options.scales.y.max = maxLoadTime;
            chart.update();
        }
    }

    function updateChart() {
        if (chart) {
            chart.data.labels = timestamps.map((_, index) => `${index + 1}`);
            chart.data.datasets[0].data = loadTimes.map(time => parseFloat(time));
            adjustYAxis(); // Adjust Y-axis to fit all data points
            chart.update();
        }
    }

    function downloadGraph() {
        const canvas = document.getElementById('load-times-chart');
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'load_times_chart.png';
        link.click();
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
                    await new Promise(resolve => setTimeout(resolve, PAUSE_TIME * 1000)); // Pause for PAUSE_TIME seconds
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

        // Update the chart with collected data if it's already initialized
        if (isGraphInitialized) {
            updateChart();
        }
    }

    function formatData(timestamps, loadTimes) {
        let csvContent = "data:text/csv;charset=utf-8,Timestamp,Load Time (Seconds)\n";
        timestamps.forEach((timestamp, index) => {
            csvContent += `${timestamp},${loadTimes[index]}\n`;
        });
        return csvContent;
    }

    function generateDownloadLink(data, filename) {
        const link = document.createElement('a');
        link.href = encodeURI(data);
        link.download = filename;
        link.click();
    }

    function calculateStatistics(loadTimes) {
        loadTimes = loadTimes.map(parseFloat);
        const countExceeding = loadTimes.filter(time => time > TIME_LINE / 1000).length;
        const mean = loadTimes.reduce((a, b) => a + b, 0) / loadTimes.length;
        const sorted = loadTimes.slice().sort((a, b) => a - b);
        const median = sorted[Math.floor(sorted.length / 2)];
        const max = Math.max(...loadTimes);
        const min = Math.min(...loadTimes);
        return { countExceeding, mean, median, max, min };
    }

    // Initialize the UI
    createUI();
})();