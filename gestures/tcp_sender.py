import socket
import sys

host = '127.0.0.1'
port = 5005
def run_tcp_sender(interval=1.0):
    data = sys.stdin.read().strip()
    if not data:
        print("❌ No data received from stdin.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode('utf-8'))
        print("✅ Data sent over TCP")

if __name__ == "__main__":
    run_tcp_sender()
