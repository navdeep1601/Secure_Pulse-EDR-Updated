import socket
import requests

def start_generic_trap(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    while True:
        client, addr = s.accept()
        requests.post("http://127.0.0.1:5000/alert", json={
            "ip": addr[0], "port": port, "service": "TCP_GENERIC", "payload": "Port Scan Detected"
        })
        client.close()
