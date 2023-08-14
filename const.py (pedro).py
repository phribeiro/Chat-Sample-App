from threading import Lock

CHAT_SERVER_HOST = "10.128.0.3"
CHAT_SERVER_PORT = 5001

registry = {"Alice":("10.128.0.2",5002), "Bob":("10.128.0.4",5002)}
registry_lock = Lock()

def get_user_address(username):
    with registry_lock:
        return registry.get(username)

def get_user_port(username):
    with registry_lock:
        return registry.get(username, (None, None))[1]

def send_message(message_pack):
    dest = message_pack[1]
    with registry_lock:
        dest_addr = registry.get(dest)
    if dest_addr is None:
        print("Error: Destination user not found")
        return
    dest_ip, dest_port = dest_addr
    client_sock = socket(AF_INET, SOCK_STREAM)
    try:
        client_sock.connect((dest_ip, dest_port))
    except:
        print("Error: Destination client is down")
        return
    marshaled_msg_pack = pickle.dumps(message_pack)
    client_sock.send(marshaled_msg_pack)
    client_sock.close()