from flask import Flask, request, session, jsonify
import netifaces


app = Flask(__name__)
app.secret_key = 'secret@dp98'


active_users=[]

@app.route('/login', methods=['POST'])
def login():
    # Retrieve IP address and other data from the request body
    data = request.json
    user_ip = data.get('ip_address')
    device = data.get('user_device')
    interfaces = data.get('network_interfaces')
    interfaces_str = ""

    # Iterate over each interface and retrieve addresses
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        # Extract the IP address from the addresses dictionary
        if netifaces.AF_INET in addresses:
            ipv4_address = addresses[netifaces.AF_INET][0]['addr']
            interfaces_str += f"Network : {interface}, Address : {ipv4_address}\n"

    # Check if the IP address is already in the list of active users
    if any(user_ip == user[0] for user in active_users):
        return jsonify({"message": "User already logged in", "ip_address": user_ip})

    # If the IP address is not in the list, add it to the list of active users
    active_users.append([user_ip, device, interfaces_str])

    return jsonify({"message": "Login successful", "ip_address": user_ip})

@app.route('/active_users', methods=['GET'])
def get_active_users():
    print(active_users)
    return jsonify({"active_users": active_users})

if __name__ == '__main__':
    app.run(port=8002)
