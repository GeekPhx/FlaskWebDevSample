from flask import Flask, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>You browser is: <br />%s .</p>' % user_agent


@app.route('/user/<name>')
def user(name):
    return '<h2>Hello , %s.</h2>' % name


if __name__ == '__main__':
    app.run()
