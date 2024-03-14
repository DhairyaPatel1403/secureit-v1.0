from flask import Flask, jsonify, request

app = Flask(__name__)

from flask import Flask, jsonify, request

app = Flask(__name__)

details = []  # List to store details


# Endpoint to add a new name
@app.route('/details', methods=['POST'])
def add_details():
    data = request.get_json()
    cipher_name = data.get('cipher_name')

    if cipher_name is not None and cipher_name=="Elgamal":
        p1 = data.get('p1')
        p = data.get('p')
        h = data.get('h')
        q = data.get('q')
        key = data.get('key')
        filename = data.get('filename')
        username = data.get('username')
        key=int(key)

        if cipher_name and p1 and p and h and q and key and filename and username:
            details.append({
                'name': cipher_name,
                'p1': p1,
                'p': p,
                'h': h,
                'q': q,
                'key':key,
                'filename' : filename,
                'username' : username
            })
            return jsonify({'message': 'Details added successfully'}), 201
        else:
            return jsonify({'error': 'All details are required'}), 400



    elif cipher_name is not None and cipher_name=="RSA":
        n = data.get('n')
        key = data.get('key')
        username = data.get('username')
        filename = data.get('filename')
        key=int(key)

        if cipher_name and n and key:
            details.append({
                'name': cipher_name,
                'n':n,
                'key':key,
                'username':username,
                'filename':filename
            })
            return jsonify({'message': 'Details added successfully'}), 201
        else:
            return jsonify({'error': 'All details are required'}), 400

    else:
        return jsonify({'error': 'All details are required'}), 400

# Endpoint to get all names
@app.route('/details', methods=['GET'])
def get_names():
    return jsonify({'details': details})

if __name__ == '__main__':
    app.run()
