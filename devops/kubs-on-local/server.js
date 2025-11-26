const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 8080;
const HOST = "0.0.0.0";

// Record the start time of the server for the readiness probe.
const serverStartTime = Date.now();

// --- Main Application Endpoints ---

// 1. Root endpoint
app.get("/", (req, res) => {
  res.send("Welcome to the Node.js sample app on Kubernetes!");
});

// 2. Liveness probe endpoint
app.get("/healthz", (req, res) => {
  // This endpoint is used by Kubernetes to check if the application is still running.
  // If it returns a 200 OK, Kubernetes knows the app is alive.
  res.status(200).send("OK");
});

// 3. Readiness probe endpoint
app.get("/readyz", (req, res) => {
  const readinessCheckDuration = 15000; // 15 seconds
  const timeSinceStart = Date.now() - serverStartTime;

  // This endpoint simulates a startup delay.
  // For the first 15 seconds, the app is "not ready" to serve traffic.
  if (timeSinceStart < readinessCheckDuration) {
    console.log("Readiness probe failed: App is still starting up.");
    // Return 500 to indicate the app is not ready yet.
    res.status(500).send("Service not ready");
  } else {
    // After 15 seconds, return 200 OK. Kubernetes will then start sending traffic to this pod.
    res.status(200).send("OK");
  }
});

// 4. ConfigMap endpoint
app.get("/config", (req, res) => {
  // This endpoint reads a configuration value injected from a Kubernetes ConfigMap.
  const greeting = process.env.GREETING_MESSAGE || "Hello (default)!";
  res.send(`Message from ConfigMap: ${greeting}`);
});

// 5. Secret endpoint
app.get("/secret", (req, res) => {
  // This endpoint reads a secret value injected from a Kubernetes Secret.
  // NOTE: Never expose secrets like this in a real application! This is for demonstration only.
  const apiKey = process.env.API_KEY || "No API Key found.";
  res.send(`My secret API Key is: ${apiKey}`);
});

// 6. Persistent data endpoint
app.get("/data", (req, res) => {
  // This endpoint demonstrates writing to and reading from a volume.
  const dataDir = "/app/data";
  const dataFile = path.join(dataDir, "temp.txt");
  const timestamp = new Date().toISOString();

  try {
    // Ensure the directory exists.
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }

    // Write the current timestamp to the file.
    fs.writeFileSync(dataFile, `Data written at: ${timestamp}\n`);
    console.log(`Successfully wrote to ${dataFile}`);

    // Read the content back from the file.
    const content = fs.readFileSync(dataFile, "utf8");
    res.send(`Read from volume: "${content.trim()}"`);
  } catch (error) {
    console.error("Failed to read/write to volume:", error);
    res.status(500).send(`Error interacting with volume: ${error.message}`);
  }
});

// 7. CPU-intensive endpoint for HPA testing
app.get("/heavy", (req, res) => {
  console.log("Starting heavy computation...");
  // This loop is intentionally inefficient to consume CPU cycles.
  // It will cause CPU utilization to spike, triggering the HorizontalPodAutoscaler.
  let result = 0;
  for (let i = 0; i < 5e9; i++) {
    // 5 billion iterations
    result += Math.sqrt(i);
  }
  console.log("Finished heavy computation.");
  res.send(`Heavy computation finished. Result (not meaningful): ${result}`);
});

app.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
  // Log when the readiness probe will become successful.
  setTimeout(() => {
    console.log("Readiness probe should now be successful.");
  }, 15000);
});
