import socket
import json

def print_routing_table(start_node, routing_table):
    print(f"라우팅 테이블 (출발지: {start_node})")
    print(f"{'목적지':<10} {'링크':<10}")
    for destination, (start, next_hop) in routing_table.items():
        print(f"{destination:<10} ({start},{next_hop})")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    # 샘플 네트워크 토폴로지 및 시작 노드
    graph = {
        'u': {'v': 2, 'w': 5, 'x': 1},
        'v': {'u': 2, 'w': 3, 'x': 2},
        'w': {'u': 5, 'v': 3, 'y': 1, 'z': 5},
        'x': {'u': 1, 'v': 2, 'y': 1},
        'y': {'x': 1, 'w': 1, 'z': 2},
        'z': {'w': 5, 'y': 2}
    }
    start_node = 'u'
    
    data = {'graph': graph, 'start': start_node}
    request = json.dumps(data)
    client.send(request.encode('utf-8'))
    
    response = client.recv(4096)
    routing_table = json.loads(response.decode('utf-8'))
    print("서버로부터 받은 라우팅 테이블:")
    
    print_routing_table(start_node, routing_table)
    
    client.close()

if __name__ == "__main__":
    main()
