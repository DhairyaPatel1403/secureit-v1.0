from flask import Flask
from push import file


app = Flask(__name__)

@app.route("/push_encrypted_file_elgamal/<file_name>/<file>/<connect_password>")
def hello_world(file_name, file, connect_password):
    if file is not None and file_name is not None:
        if file_name!="" and file!="":
            if connect_password == '123abc':
                return f"Hello, World! Parameter received: {file_name}"
            else:
                return "Incorrect Password 🚨"

    else:
        return "Incorrect"