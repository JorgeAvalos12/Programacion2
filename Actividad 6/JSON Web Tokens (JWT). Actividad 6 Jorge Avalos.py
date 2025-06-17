from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'

usuarios = {
    "usuario1": "contraseña1",
    "usuario2": "contraseña2"
}


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')

    if username in usuarios and usuarios[username] == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Credenciales inválidas'}), 401


@app.route('/protegido', methods=['GET'])
def protegido():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token es necesario'}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Bienvenido {data["user"]}'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido'}), 401

if __name__ == '__main__':
    app.run(debug=True)
