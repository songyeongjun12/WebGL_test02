from flask import Flask, request, redirect, render_template,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite 데이터베이스 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 (User 테이블)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# 애플리케이션 시작 시 데이터베이스와 테이블 생성
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/users')
def show_users():
    # 모든 사용자 데이터 가져오기
    users = User.query.all()
    return render_template('users.html', users=users)

# 홈 페이지
@app.route('/')
def home():
    return render_template('home.html')

# 게임 페이지
@app.route('/game')
def game():
    return render_template('index.html')

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 패스워드 해시화
        hashed_password = generate_password_hash(password, method='sha256')

        # 새로운 사용자 객체 생성
        new_user = User(username=username, email=email, password=hashed_password)

        # 데이터베이스에 저장
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')  # 회원가입 후 로그인 페이지로 리다이렉트

    return render_template('signup.html')

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()  # 이메일로 사용자 조회
        if user and check_password_hash(user.password, password):  # 패스워드 확인
            return redirect('/game')  # 로그인 성공 후 게임 페이지로 이동
        else:
            return "Invalid login credentials", 401  # 로그인 실패 시 오류 메시지 표시

    return render_template('login.html')

# 파일 서빙
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('static/Build', filename)

if __name__ == "__main__":
    app.run(debug=True)
