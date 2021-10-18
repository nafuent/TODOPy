from flask import  request,make_response,redirect,render_template,session,url_for
from flask.helpers import flash

import unittest

from app import create_app
from app.forms import LoginForm

from app.firestore_service import get_users, get_todos


# Initialitation
app =create_app()

todos =['Comparar cafe','Aprender Fask', 'Crear TODO app']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


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

@app.route('/hello',methods = ['GET'])
def hello():
    #user_ip=request.cookies.get('user_ip')
    user_ip = session.get('user_ip')

    username=session.get('username')

    #contexto
    context = {
        'user_ip':user_ip,
        'todos':get_todos(user_id=username),
        #'login_form':login_form,
        'username':username
    }

    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('hello.html',**context)

# main process
if __name__ == '__main__':
    app.run(port = 5000, debug = True)



