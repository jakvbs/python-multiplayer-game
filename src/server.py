from typing import Literal
import socket
import pickle
from game import Game
import threading


PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


games: dict[int, Game] = {}


def handle_client(conn: socket.socket, p: Literal[1, 2], game_id: int) -> None:
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        x, y = data.split(",")
                        if game.current_player == p:
                            game.handle_click(int(x), int(y))

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception:
            break

    print(f"[DISCONNECTED] {p}")
    try:
        del games[game_id]
        print(f"[CLOSED] game {game_id}")
    except Exception as ex:
        print(ex)

    conn.close()


def main() -> None:
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        active_count = threading.active_count()
        p = 1
        game_id = (active_count - 1) // 2
        if active_count % 2 == 1:
            games[game_id] = Game()
            print(f"[NEW GAME] new game {game_id} started")
        else:
            games[game_id].ready = True
            p = 2

        thread = threading.Thread(
            target=handle_client, args=(conn, p, game_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {active_count}")


if __name__ == "__main__":
    main()
