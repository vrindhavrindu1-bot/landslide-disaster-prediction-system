// Create the map
var map = L.map('map').setView([10.8505, 76.2711], 7); // Kerala

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Add a marker

function goHome() {
    window.location.href = "index.html";
}

function goReport() {
    window.location.href = "report.html";
}

function goAlerts() {
    window.location.href = "alerts.html";
}
// Get saved report data
var savedData = localStorage.getItem("reportData");

if (savedData) {

    var data = JSON.parse(savedData);

    // Random demo coordinates
    

    var marker = L.marker([lat, lng]).addTo(map);

    marker.bindPopup(
        "<b>Location:</b> " + data.location +
        "<br><b>Risk:</b> " + data.risk
    );
}
var reports = JSON.parse(localStorage.getItem("reports")) || [];

reports.forEach(function(data) {

    var marker = L.marker([data.latitude, data.longitude]).addTo(map);

    marker.bindPopup(
        "<b>Location:</b> " + data.location +
        "<br><b>Risk:</b> " + data.risk +
        "<br><b>Time:</b> " + data.time
    );
});
function submitReport() {

    let location = document.getElementById("location").value;

    if(location === "") {
        document.getElementById("message").innerHTML = "Please enter location!";
        return;
    }

    document.getElementById("message").innerHTML = 
        "Report submitted successfully for " + location + "!";
}
var selectedRisk = "Medium";

function setRisk(button, level) {

    selectedRisk = level;

    var buttons = document.querySelectorAll(".severity-btn");

    buttons.forEach(btn => btn.classList.remove("active"));

    button.classList.add("active");
}
function predictRisk(){
    let rainfall = document.getElementById("rainfall").value;
    let slope = document.getElementById("slope").value;
fetch("http://127.0.0.1:5000/predict-risk", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        rainfall: parseFloat(rainfall),
        slope: parseFloat(slope)
    })
})
.then(response => response.json())
.then(data => {
    document.getElementById("result").innerText =
    "Risk level:" + data.risk_level;
});
}