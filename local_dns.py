import socket
import json
import threading

local_dns_table = {
    "example.com": "93.184.216.34",
    "localhost": "127.0.0.1"
}

def query_local_dns(domain):
    return local_dns_table.get(domain, None)

def add_domain(domain, ip):
    local_dns_table[domain] = ip
    return f"Domain {domain} IP {ip} 추가"

def handle_client(c_sock, tld_dns_host, tld_dns_port):
    try:
        while True:
            read_data = c_sock.recv(1024)
            if not read_data:
                break

            request = json.loads(read_data.decode())
            action = request.get("action")
            domain = request.get("domain")

            if action == "query":
                ip = query_local_dns(domain)
                if ip is None:
                    print(f"{domain} not found in local DNS, 상위 DNS에 query")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tld_sock:
                        tld_sock.connect((tld_dns_host, tld_dns_port))
                        tld_sock.sendall(json.dumps(request).encode())
                        ip = tld_sock.recv(1024).decode()
                    if ip == "Error: Domain not found":
                        c_sock.sendall(ip.encode())
                    else:
                        c_sock.sendall(ip.encode())
                else:
                    c_sock.sendall(ip.encode())
            elif action == "add":
                ip = request.get("ip")
                response = add_domain(domain, ip)
                c_sock.sendall(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c_sock.close()

def start_local_dns_server(host='127.0.0.1', port=9701, tld_dns_host='127.0.0.1', tld_dns_port=9702):
    print("1. 소켓 생성")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("2. 바인딩")
    sock.bind((host, port))

    print("3. 접속 대기")
    sock.listen()

    print(f"Local DNS server 시작 정보 {host}:{port}")

    while True:
        c_sock, addr = sock.accept()
        print(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client, args=(c_sock, tld_dns_host, tld_dns_port))
        client_thread.start()

    sock.close()

if __name__ == "__main__":
    start_local_dns_server()
