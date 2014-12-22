from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/medium')
def editor():
    return render_template('med.html')

if __name__ == '__main__':
    app.run()
