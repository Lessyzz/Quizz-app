from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import string, random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

username = ""
rooms = {}

#region Web Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global username
        username = request.form['username']

        karakterler = string.ascii_letters + string.digits
        roomid = ''.join(random.choice(karakterler) for _ in range(5))
    
        return redirect(url_for('createroom', roomid = roomid))
    return render_template('index.html')

@app.route('/createroom/<roomid>')
def createroom(roomid):
    return redirect(url_for('game', roomid = roomid))

@app.route('/game/<roomid>')
def game(roomid):
    if roomid not in rooms: # Bu kişi admin oluyor
        rooms[roomid] = username
        return render_template('admin.html', username=username, roomid=roomid)
    else: # Burada Oyuncu oluyor
        return render_template('game.html', username=username, roomid=roomid)

#endregion

#region SocketIO Events

@socketio.on('chat_message')
def handle_chat_message(msg):
    emit('chat_message', "gelen mesaj: " + msg, broadcast=True)

#endregion

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)