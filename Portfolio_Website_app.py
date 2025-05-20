# copyright [2025] [Phat Nguyen Cong] (Github: https://github.com/paht2005)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from projects_data import projects

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_key'

# Cấu hình DB, đặt file trong thư mục instance để bảo mật
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model dự án portfolio
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Model phản hồi liên hệ
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Tạo bảng nếu chưa có
with app.app_context():
    db.create_all()

# Trang chủ, hiện các dự án nổi bật
@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Trang tất cả dự án
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

# Trang giới thiệu
@app.route('/about')
def about():
    return render_template('about.html')

# Trang liên hệ + gửi phản hồi
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not (name and email and message):
            flash('Please fill out all fields.', 'error')
        else:
            feedback = Feedback(name=name, email=email, message=message)
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your message!', 'success')
            return redirect(url_for('home'))
    return render_template('contact.html')

# Trang xem tất cả feedback gửi về
@app.route('/feedback')
def view_feedback():
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
