import socket

def start_client(host='127.0.0.1', port=9700):
    print("1. 소켓 생성")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("3. 접속 시도")
    sock.connect((host, port))

    while True:
        expression = input("수식 입력 (종료 원하면 'exit' 입력): ")
        if expression.lower() == 'exit':
            break

        print("5. 데이터 송신")
        sock.sendall(expression.encode())

        data = sock.recv(1024)
        print(f"Result: {data.decode()}")

    print("6. 접속 종료")
    sock.close()

if __name__ == "__main__":
    start_client()
