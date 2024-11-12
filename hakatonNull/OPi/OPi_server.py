import cv2
import socket
import pickle
import struct

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5000))  # 0.0.0.0 для прослушивания на всех интерфейсах
print("port opened\n")
server_socket.listen(5)

client_socket, addr = server_socket.accept()
print(f"connection from: {addr}\n")

data = b""
payload_size = struct.calcsize("Q")


while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # Чтение данных порциями
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Декодируем кадр
    frame = pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("Receiving Video", frame)

    if cv2.waitKey(1) == ord("q"):
        break

client_socket.close()
server_socket.close()
