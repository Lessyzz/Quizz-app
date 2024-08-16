from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import string, random, sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}
roomusers = []
roomuserpoints = {}

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

@app.route('/admin')
def yonetici():
    roomid = createRoomVoid()
    return redirect(url_for('createroom', roomid = roomid))

@app.route('/createroom/<roomid>')
def createroom(roomid):
    return redirect(url_for('game', roomid = roomid))

#endregion

#region Player

@app.route('/player', methods=['GET', 'POST'])
def oyuncu():
    if request.method == 'POST':
        roomid = request.form['roomid']
        return redirect(url_for('joinroom', roomid = roomid))
    return render_template('player.html')

@app.route('/joinroom/<roomid>')
def joinroom(roomid):
    if roomid not in rooms:
        return "Oda bulunamadı"
    return redirect(url_for('login', roomid = roomid))
    
@app.route('/login/<roomid>', methods=['GET', 'POST'])
def login(roomid):
    if request.method == 'POST':
        session["username"] = request.form['username']
        return redirect(url_for('game', roomid = roomid))
    return render_template('login.html', roomid=roomid)
#endregion

@app.route('/game/<roomid>')
def game(roomid):
    if roomid not in rooms:                     # Bu kişi admin oluyor
        rooms[roomid] = "token"
        session["username"] = "admin"
        return render_template('admin.html', username=session["username"], roomid=roomid)
    else:                                       # Burada Oyuncu oluyor
        roomusers.append(session["username"])
        roomuserpoints[session["username"]] = 0
        return render_template('game.html', username=session["username"], roomid=roomid)

@socketio.on('answer')
def handle_answer(data):
    global roomuserpoints
    answer = data['answer']
    if answer == data['correct_answer']:
        roomuserpoints[data['username']] += data['point'] # değiştir
    emit('answer', roomuserpoints, broadcast=True)
#endregion

#region SocketIO Events

@socketio.on('chat_message')
def handle_chat_message(msg):
    emit('chat_message', "gelen mesaj: " + msg, broadcast=True)

@socketio.on('start_game')
def handle_start_game(data):
    ders_adi = data['ders_adi']
    konu_adi = data['konu_adi']
    test_adi = data['test_adi']
    sorular = databaseProcess(ders_adi, konu_adi, test_adi)
    emit('start_game', sorular, broadcast=True)
#endregion

#region DatabaseProcesses

def databaseProcess(ders_adi, konu_adi, test_adi):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    #ders_adi = 'Matematik'
    #konu_adi = 'Cebir'
    #test_adi = 'Cebir Test 1'

    # Sorgu
    cursor.execute('''
        SELECT Sorular.soru_metni, Sorular.cevap
        FROM Sorular
        JOIN Testler ON Sorular.test_id = Testler.id
        JOIN Konular ON Testler.konu_id = Konular.id
        JOIN Dersler ON Konular.ders_id = Dersler.id
        WHERE Dersler.ders_adi = ? AND Konular.konu_adi = ? AND Testler.test_adi = ?
    ''', (ders_adi, konu_adi, test_adi))

    # Sonuçları al ve yazdır
    sorular = cursor.fetchall()
    conn.close()

    return sorular

    # for soru in sorular:
    #     print(f"Soru: {soru[0]}")
    #     print(f"Cevap: {soru[1]}")
    #     print("---")

#endregion

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)