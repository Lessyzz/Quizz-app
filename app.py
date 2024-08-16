from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('game', username=request.form['username']))
    return render_template('index.html')

@app.route('/game/<username>')
def game(username):
    return render_template('game.html', username=username)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)