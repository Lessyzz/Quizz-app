from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import string, random, sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

username = ""
rooms = {}

#region Functions

def createRoomVoid():
    chars = string.ascii_letters + string.digits
    roomid = ''.join(random.choice(chars) for _ in range(5))

    while roomid in rooms:
        roomid = ''.join(random.choice(chars) for _ in range(5))
    return roomid

#endregion

#region Web Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#region Admin

@app.route('/yonetici')
def yonetici():
    roomid = createRoomVoid()
    return redirect(url_for('createroom', roomid = roomid))

@app.route('/createroom/<roomid>')
def createroom(roomid):
    return redirect(url_for('game', roomid = roomid))

#endregion

#region Player

@app.route('/oyuncu', methods=['GET', 'POST'])
def oyuncu():
    if request.method == 'POST':
        roomid = request.form['roomid']
        return redirect(url_for('joinroom', roomid = roomid))
    return render_template('oyuncu.html')

@app.route('/joinroom/<roomid>')
def joinroom(roomid):
    return redirect(url_for('login', roomid = roomid))
    
@app.route('/login/<roomid>', methods=['GET', 'POST'])
def login(roomid):
    if request.method == 'POST':
        global username
        username = request.form['username']
        return redirect(url_for('game', roomid = roomid))
    return render_template('login.html', roomid=roomid)
#endregion

@app.route('/game/<roomid>')
def game(roomid):
    if roomid not in rooms:                     # Bu kişi admin oluyor
        rooms[roomid] = "token"
        return render_template('admin.html', username=username, roomid=roomid)
    else:                                       # Burada Oyuncu oluyor
        return render_template('game.html', username=username, roomid=roomid)

#endregion

#region SocketIO Events

@socketio.on('chat_message')
def handle_chat_message(msg):
    emit('chat_message', "gelen mesaj: " + msg, broadcast=True)

#endregion

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)