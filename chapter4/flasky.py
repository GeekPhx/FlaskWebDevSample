# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session,\
                         redirect, url_for, flash

from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, DataRequired

from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'we_need_to_update_secret_key'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    # DataRequired instead of Required
    name = StringField("可以告诉谦虚的我, 您叫什么名字吗?", validators=[DataRequired()])
    submit = SubmitField('既然你这么谦虚, 告诉你吧!')


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', ua=user_agent, current_time=datetime.utcnow())


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('您好像改变了您的名字!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user', name=session.get('name')))
    return render_template('echo.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
