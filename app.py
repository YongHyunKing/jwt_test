from flask import Flask, request, jsonify, make_response, render_template, session, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps

# secret_key 생성
# import uuid
# uuid.uuid4().hex
# import secrets
# secrets.token_urlsafe(12)

app = Flask(__name__)
datetime_format = "%Y-%m-%d %H:%M:%S.%f"
app.config['SECRET_KEY'] = 'cc9b2c4459dd475fac8bc6074ba3cf5c'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        # 토큰이 없는 경우
        if not token:
            return render_template('login.html')
        try:
            payload = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(payload)
            # 토큰의 유효기간이 다 된 경우
            if 'expiration' in payload:
                datetime_result = datetime.strptime(
                    payload['expiration'], datetime_format)
                if datetime_result < datetime.utcnow()+timedelta(hours=9):
                    print("token expired")
                    return render_template('login.html')
            else:
                print("no expiration time in token")
                return render_template('login.html')
            print(payload)
        # 이상한 값이 들어왔을 경우
        except jwt.exceptions.InvalidTokenError:
            print("invalid token")
            return render_template('login.html')
        return func(payload['user'], *args, **kwargs)

    return decorated
# Home


@app.route('/')
@token_required
def home(user):
    return render_template('main.html', email=user)


# login
@app.route('/login', methods=['POST'])
def login():
    if request.form['give_email'] and request.form['give_password'] == '123456':
        time = datetime.utcnow()
        add_time = timedelta(hours=9, seconds=30)
        token = jwt.encode({
            'user': request.form['give_email'],
            'expiration': str(time+add_time)
        },
            app.config['SECRET_KEY'])
        resp = make_response({'result': 'success'})

        resp.set_cookie('token', token, httponly=True)
        print(token)
        return resp
    else:
        return make_response({'result': 'fail'})

# logout route


@app.route('/logout', methods=['POST'])
def logout():
    response = make_response({'result': 'success'})
    response.set_cookie('token', '', expires=0)
    return response


if __name__ == "__main__":
    app.run(debug=True)
