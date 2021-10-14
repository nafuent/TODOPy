from flask import Flask, request,make_response,redirect,render_template,session,url_for
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

# Initialitation
app =Flask(__name__)
booststrap = Bootstrap(app)

app.config['SECRET_KEY']='SUPER SECRETO'


todos =['Comparar cafe','Aprender Fask', 'Crear TODO app']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')


# error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error,code=400)

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html',error = error, code=500)

# routes
@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    #response.set_cookie('user_ip',user_ip)
    return response

@app.route('/hello',methods = ['GET','POST'])
def hello():
    #user_ip=request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username=session.get('username')

    #contexto
    context = {
        'user_ip':user_ip,
        'todos':todos,
        'login_form':login_form,
        'username':username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con exito!')
        return redirect(url_for('index'))

    return render_template('hello.html',**context)

# main process
if __name__ == '__main__':
    app.run(port = 5000, debug = True)



