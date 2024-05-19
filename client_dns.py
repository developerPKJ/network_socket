import socket
import json

def query_dns(domain):
    return {"action": "query", "domain": domain}

def add_domain(domain, ip):
    return {"action": "add", "domain": domain, "ip": ip}

def start_client(dns_host='127.0.0.1', dns_port=9701):
    while True:
        command = input("명령어 입력 (query/add/exit): ")
        if command == "exit":
            break
        elif command == "query":
            domain = input("도메인 입력: ")
            request = query_dns(domain)
        elif command == "add":
            domain = input("도메인 입력: ")
            ip = input("IP 입력: ")
            request = add_domain(domain, ip)
        else:
            print("잘못된 명령어")
            continue

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print("1. 소켓 생성")
            print("3. 접속 시도")
            sock.connect((dns_host, dns_port))

            print("5. 데이터 송신")
            sock.sendall(json.dumps(request).encode())
            response = sock.recv(1024)
            print(f"Response: {response.decode()}")

if __name__ == "__main__":
    start_client()
