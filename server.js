const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const puppeteer = require('puppeteer');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let browser, page;

// Start the browser instance
async function startBrowser() {
  browser = await puppeteer.launch({ headless: false });
  page = await browser.newPage();
  await page.goto('https://example.com'); // Default page
}

// Handle WebSocket connections
wss.on('connection', (ws) => {
  console.log('A user connected');

  // Navigate to a new URL
  ws.on('message', async (message) => {
    const data = JSON.parse(message);

    if (data.type === 'navigate') {
      await page.goto(data.url);
      ws.send(JSON.stringify({ type: 'url-update', url: data.url }));
    }

    // Handle clicks
    if (data.type === 'click') {
      await page.mouse.click(data.x, data.y);
    }

    // Handle typing
    if (data.type === 'type') {
      await page.keyboard.type(data.text);
    }

    // Handle scrolling
    if (data.type === 'scroll') {
      await page.evaluate((deltaY) => {
        window.scrollBy(0, deltaY);
      }, data.deltaY);
    }
  });

  // Disconnect
  ws.on('close', () => {
    console.log('User disconnected');
  });
});

// Serve the frontend
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Start the server
server.listen(3000, async () => {
  console.log('Server running on http://localhost:3000');
  await startBrowser();
});