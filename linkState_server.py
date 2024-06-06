import socket
import json
import heapq

def dijkstra(graph, start):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return distances, previous_nodes

def get_routing_table(previous_nodes, start):
    routing_table = {}
    for destination in previous_nodes:
        if destination == start:
            continue
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        routing_table[destination] = (start, path[1]) if len(path) > 1 else (start, start)
    return routing_table

def handle_client(client_socket):
    request = client_socket.recv(4096)
    data = json.loads(request.decode('utf-8'))
    graph = data['graph']
    start_node = data['start']
    distances, previous_nodes = dijkstra(graph, start_node)
    routing_table = get_routing_table(previous_nodes, start_node)
    response = json.dumps(routing_table)
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("서버가 9999 포트에서 대기 중입니다.")
    while True:
        client_socket, addr = server.accept()
        print(f"{addr}로부터 연결을 수락했습니다.")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
