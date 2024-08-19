from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import sqlite3
from random_word import RandomWords

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}
roomusers = []
roomuserpoints = {}
roomnames = []

#region Functions

r = RandomWords()

def createRoomVoid():
    word = r.get_random_word()

    while word in rooms:
        word = r.get_random_word()
    return word

def getLessons():
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    lessons = cursor.execute('SELECT * FROM Dersler').fetchall()
    return lessons

def getTopics(lesson_id):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    topics = cursor.execute('SELECT * FROM Konular WHERE ders_id = ?', (lesson_id,)).fetchall()
    return topics

def getTests(topic_id):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    tests = cursor.execute('SELECT * FROM Testler WHERE konu_id = ?', (topic_id,)).fetchall()
    return tests

def getQuestions(test_id):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    questions = cursor.execute('SELECT * FROM Sorular WHERE test_id = ?', (test_id,)).fetchall()
    return questions

def getAnswers(question_id):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    answers = cursor.execute('SELECT sik FROM Sıklar').fetchall()
    return answers

def getCorrectAnswer(question_id):
    conn = sqlite3.connect('Database.sql')
    cursor = conn.cursor()

    correct_answer = cursor.execute('SELECT dogru_sik FROM Sorular WHERE id = ?', (question_id,)).fetchone()
    correct_answer = int(correct_answer[0])
    return correct_answer

def getRooms():
    return rooms

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
        return redirect(url_for('joinroom', roomid = roomid, roomnames = roomnames))
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
        return redirect(url_for('selectcharacter', roomid = roomid))
    return render_template('login.html', roomid=roomid)

@app.route('/selectcharacter/<roomid>', methods=['GET', 'POST'])
def selectcharacter(roomid):
    if request.method == 'POST':
        session["character"] = request.form['character']
        return redirect(url_for('game', roomid = roomid))
    return render_template('selectcharacter.html')
#endregion

@app.route('/game/<roomid>')
def game(roomid):
    if roomid not in rooms:                     # Bu kişi admin oluyor
        rooms[roomid] = "token"
        roomnames.append(roomid)
        session["username"] = "admin"
        lessons = getLessons()
        return render_template('admin.html', username=session["username"], roomid=roomid, lessons=lessons)
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

@socketio.on('start_game')
def handle_chat_message(msg):
    emit('start_game', "start", broadcast=True)

@socketio.on('select_lesson')
def handle_lesson(msg):
    emit('select_topic', getTopics(msg), broadcast=True)

@socketio.on('select_topic')
def handle_topic(msg):
    emit('select_test', getTests(msg), broadcast=True)

@socketio.on('select_test')
def handle_test(msg):
    emit('get_questions_and_answers', [getQuestions(msg), getAnswers(msg)], broadcast=True)
    
@socketio.on('broadcast_question_to_players')
def broadcast_question_to_players(msg):
    question_id = msg[0]
    question_number = msg[1]
    question = msg[2]
    answers = msg[3]
    duration = msg[4]
    emit('get_question_as_player', [question_id, question_number, question, answers, duration], broadcast=True)

@socketio.on('give_answer') # Handle answers
def handle_answer(msg):
    isTrue = False

    if msg[1] + 1 == getCorrectAnswer(msg[0]): # Doğru mu yanlış mı kontrol et msg[1] + 1 çünkü cevap indexi 0 dan başlıyor doğru cevap indexi 1 den başlıyor
        isTrue = True
    emit('check_answer', isTrue, broadcast=True)

#endregion

@app.route('/addtodatabase', methods=['GET', 'POST'])
def manage_data():
    conn = sqlite3.connect('Database.sql')

    if request.method == 'POST':
        ders_ad = request.form.get('ders_ad')
        konu_ad = request.form.get('konu_ad')
        test_ad = request.form.get('test_ad')
        soru = request.form.get('soru')
        dogru_sik = request.form.get('dogru_sik')
        sure_sn = request.form.get('sure_sn')
        siklar = request.form.getlist('siklar')

        # Ders ekleme veya mevcut ders ID'sini alma
        ders = conn.execute('SELECT * FROM Dersler WHERE ad = ?', (ders_ad,)).fetchone()
        if ders is None:
            conn.execute('INSERT INTO Dersler (ad) VALUES (?)', (ders_ad,))
            ders_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        else:
            ders_id = ders[0]

        # Konu ekleme veya mevcut konu ID'sini alma
        konu = conn.execute('SELECT * FROM Konular WHERE ad = ? AND ders_id = ?', (konu_ad, ders_id)).fetchone()
        if konu is None:
            conn.execute('INSERT INTO Konular (ad, ders_id) VALUES (?, ?)', (konu_ad, ders_id))
            konu_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        else:
            konu_id = konu[0]

        # Test ekleme veya mevcut test ID'sini alma
        test = conn.execute('SELECT * FROM Testler WHERE ad = ? AND konu_id = ?', (test_ad, konu_id)).fetchone()
        if test is None:
            conn.execute('INSERT INTO Testler (ad, konu_id) VALUES (?, ?)', (test_ad, konu_id))
            test_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        else:
            test_id = test[0]

        # Soru ekleme
        conn.execute('INSERT INTO Sorular (test_id, soru, dogru_sik, sure_sn) VALUES (?, ?, ?, ?)', (test_id, soru, dogru_sik, sure_sn))
        soru_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        # Şıklar ekleme
        for sik in siklar:
            conn.execute('INSERT INTO Sıklar (soru_id, sik) VALUES (?, ?)', (soru_id, sik))

        conn.commit()

    dersler = conn.execute('SELECT * FROM Dersler').fetchall()
    conn.close()

    return render_template('addtodatabase.html', dersler=dersler)

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000)