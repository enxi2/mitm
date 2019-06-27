// Usage
if (process.argv.length < 3) {
    console.log("Usage: node move.js <locations>");
    process.exit(1);
}

// Imports
const http = require("http");
const fs = require("fs");

// Constants
// 0.00505370141579543 degrees is a 5 minute walk
// About 1.6845671385984767e-05 degrees per second
const WALK_MULTIPLIER = 1.5;
const WALK_SPEED = 1.6845671385984767e-05 * WALK_MULTIPLIER;

// Functions
function dist(a, b) {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    return Math.sqrt(dx * dx + dy * dy);
}

function interp(t, a, b) {
    return [
        a[0] * (1.0 - t) + b[0] * t,
        a[1] * (1.0 - t) + b[1] * t
    ];
}

function discretize(locations) {
    const points = [locations[0]];
    let index = 0;
    let t = 0;
    while (index < locations.length - 1) {
        let distance = dist(locations[index], locations[index + 1]);
        let dt = WALK_SPEED / distance;
        t += dt;
        let nextPoint = interp(t, locations[index], locations[index + 1]);
        points.push(nextPoint);
        if (t >= 1) {
            t = 0;
            index++;
        }
    }
    return points;
}


// Read locations from file
const locationFile = process.argv[2];
const lines = fs.readFileSync(locationFile).toString();
const locations = [];
lines.split("\n").forEach(l => {
    const comma = l.indexOf(",");
    if (comma >= 0) {
        locations.push([
            parseFloat(l.substring(0, comma)),
            parseFloat(l.substring(comma + 1))
        ]);
    }
});

if (locations.length == 0) {
    console.log("Error: No locations found. Make sure locations are in LATITUDE, LONGITUDE format.");
    process.exit(1);
}

// Looping
const loop = locationFile.indexOf("loop") >= 0;
if (loop) {
    locations.push(locations[0]);
}
console.log("Read " + locations.length + " locations");

// Convert locations into points (one point = one second to reach
const points = discretize(locations);
const pointsLength = points.length - 1;
console.log("Generated " + points.length + " points");

let startTime = Date.now();
let pauseTime = -1;
const server = http.createServer((req, res) => {
    if (req.url == "/pause") {
        res.writeHead(200, { "Content-Type": "text/plain" });
        if (pauseTime < 0) {
            pauseTime = Date.now();
            res.end("paused");
        }
        else {
            startTime += Date.now() - pauseTime;
            pauseTime = -1;
            res.end("unpaused");
        }
    }
    else {
        let currentTime = (Date.now() - startTime) / 1000.0;
        if (pauseTime >= 0) {
            currentTime = (pauseTime - startTime) / 1000.0;
        }
        let index = Math.floor(currentTime) | 0;
        let t = currentTime - index;
        if (loop) {
            index = index % pointsLength;
        }
        else {
            let round = Math.floor(index / pointsLength) | 0;
            if (round % 2 == 1) { // Forward
                index = index % pointsLength;
            }
            else { // Backward
                index = pointsLength - (index % pointsLength) - 1;
                t = 1.0 - t;
            }
        }
        
        let loc = interp(t, points[index], points[index + 1]);
        res.writeHead(200, { "Content-Type": "text/plain" });
        res.end(loc[0].toFixed(8) + "      " + loc[1].toFixed(8) + "        ");
    }
});

console.log("Listening");
server.listen(8080);
