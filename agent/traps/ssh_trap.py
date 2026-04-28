import socket
import requests

def start_ssh_trap(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    while True:
        client, addr = s.accept()
        # Fake SSH Banner
        client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\n")
        data = client.recv(1024).decode(errors='ignore')
        
        # Log to Backend
        requests.post("http://127.0.0.1:5000/alert", json={
            "ip": addr[0], "port": port, "service": "SSH", "payload": data or "SSH Scanner"
        })
        client.close()
