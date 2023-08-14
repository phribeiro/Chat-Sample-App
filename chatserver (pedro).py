from socket import *
import pickle
import const

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(('0.0.0.0', const.CHAT_SERVER_PORT))
server_sock.listen(5)

print("Chat Server is ready...")

def handle_client(conn):
    marshaled_msg_pack = conn.recv(1024)
    msg_pack = pickle.loads(marshaled_msg_pack)
    msg = msg_pack[0]
    dest = msg_pack[1]
    src = msg_pack[2]
    print("RELAYING MSG: " + msg + " - FROM: " + src + " - TO: " + dest)
    
    dest_addr = const.get_user_address(dest)
    if dest_addr is None:
        conn.send(pickle.dumps("NACK"))
        return
    
    conn.send(pickle.dumps("ACK"))
    conn.close()

    client_sock = socket(AF_INET, SOCK_STREAM)
    dest_ip, dest_port = dest_addr
    try:
        client_sock.connect((dest_ip, dest_port))
    except:
        print("Error: Destination client is down")
        return

    msg_pack = (msg, src)
    marshaled_msg_pack = pickle.dumps(msg_pack)
    client_sock.send(marshaled_msg_pack)
    marshaled_reply = client_sock.recv(1024)
    reply = pickle.loads(marshaled_reply)
    if reply != "ACK":
        print("Error: Destination client did not receive message properly")
    client_sock.close()

while True:
    (conn, addr) = server_sock.accept()
    threading.Thread(target=handle_client, args=(conn,)).start()