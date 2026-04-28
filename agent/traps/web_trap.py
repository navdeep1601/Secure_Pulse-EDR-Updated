import socket
import requests

def start_web_trap(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    while True:
        client, addr = s.accept()
        # Fake Apache Header
        response = "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\nContent-Type: text/html\r\n\r\n"
        response += "<html><body><h1>Admin Login</h1><form>User: <input><br>Pass: <input type='password'></form></body></html>"
        client.send(response.encode())
        
        requests.post("http://127.0.0.1:5000/alert", json={
            "ip": addr[0], "port": port, "service": "HTTP", "payload": "Web Browser Access"
        })
        client.close()
