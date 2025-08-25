import network
import socket
import time

counter = 0

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="lights domain", password="bloodforthebloodgod",authmode=network.AUTH_WPA_WPA2_PSK)

print("Access Point Active")
print("SSID:", ap.config('essid'))
print("IP Address:", ap.ifconfig()[0])

html = """<!DOCTYPE html>
<html>
<head>
<title>ESP32 Counter</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: sans-serif; text-align: center; padding: 50px; background-color:#111; color:#fff; }
#counter { font-size:50px; margin:20px; }
button { padding:15px 30px; font-size:20px; cursor:pointer; border-radius:10px; }
</style>
</head>
<body>
<h1>Real-Time Counter</h1>
<div id="counter">0</div>
<button onclick="increment()">Increment</button>

<script>
async function fetchCounter() {
    let response = await fetch('/get');
    let data = await response.json();
    document.getElementById('counter').innerText = data.counter;
}

async function increment() {
    await fetch('/increment');
    await fetchCounter();
}

// Auto-refresh counter every 1 second
setInterval(fetchCounter, 1000);
fetchCounter();
</script>
</body>
</html>
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)
print("Server running at http://%s/" % ap.ifconfig()[0])

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    
    if "/increment" in request:
        counter += 1
        response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"counter": %d}' % counter
        conn.send(response)
    elif "/get" in request:
        response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"counter": %d}' % counter
        conn.send(response)
    else:
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.sendall(html)
    
    conn.close()
