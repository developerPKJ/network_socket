import socket

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return str(result)
    #잘못된 경우 에러출력
    except Exception as e:
        return f"Error: {str(e)}"

def start_server(host='127.0.0.1', port=9700):
    print("1. 소켓 생성")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("2. 바인딩")
    sock.bind((host, port))

    print("3. 접속 대기")
    sock.listen()

    print("4. 접속 수락")
    c_sock, addr = sock.accept()
    with c_sock:
        print(f"호스트 정보 {addr}")

        while True:
            print("5. 데이터 수신")
            read_data = c_sock.recv(1024)
            if not read_data:
                break

            expression = read_data.decode()
            print(f"수신: {expression}")

            result = evaluate_expression(expression)
            print(f"연산 결과: {result}")

            c_sock.sendall(result.encode())

    print("6. 접속 종료")
    sock.close()

if __name__ == "__main__":
    start_server()
