import socket
import json
import threading

tld_dns_table = {
    "google.com": "142.250.190.46",
    "naver.com": "104.18.28.97"
}

def query_tld_dns(domain):
    return tld_dns_table.get(domain, "Error: Domain not found")

def handle_client(c_sock):
    try:
        while True:
            read_data = c_sock.recv(1024)
            if not read_data:
                break

            request = json.loads(read_data.decode())
            domain = request.get("domain")
            ip = query_tld_dns(domain)
            print(f"Query: {domain}, Response: {ip}")
            c_sock.sendall(ip.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c_sock.close()

def start_tld_dns_server(host='127.0.0.1', port=9702):
    print("1. 소켓 생성")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("2. 바인딩")
    sock.bind((host, port))

    print("3. 접속 대기")
    sock.listen()

    print(f"tld DNS server 시작 정보 {host}:{port}")

    while True:
        c_sock, addr = sock.accept()
        print(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client, args=(c_sock,))
        client_thread.start()

    sock.close()

if __name__ == "__main__":
    start_tld_dns_server()
