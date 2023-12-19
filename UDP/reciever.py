import cv2
import socket
import numpy as np

max_length = 65507

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("10.20.54.11", 9999))

frame = None

print("-> waiting for connection")

while True:
    data, address = sock.recvfrom(max_length)
    buffer = {}

    if len(data) < 100:
        nums_of_packs = int.from_bytes(data)

        if nums_of_packs:
            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)
                buffer[i] = data

            buffered_frame = b"".join(buffer.values())

            if buffered_frame[:2] == b"\xff\xd8" and buffered_frame[-2:] == b"\xff\xd9":
                frame = np.frombuffer(buffered_frame, dtype=np.uint8)
                frame = frame.reshape(frame.shape[0], 1)

                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if frame is not None and isinstance(frame, np.ndarray):
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.imshow("Stream", frame)
                    sock.sendto(b"ACK", address)
                    if cv2.waitKey(1) == 27:
                        break

print("goodbye")
