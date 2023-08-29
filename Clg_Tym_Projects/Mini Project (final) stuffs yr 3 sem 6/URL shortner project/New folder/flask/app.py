from flask import Flask, render_template, request, redirect
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)


class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(255), unique=True, nullable=False)
    original_url = db.Column(db.String(255), nullable=False)
    expiration_timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<URLMapping short_url={self.short_url} original_url={self.original_url}>'


@app.route('/')
def home():
    return render_template('login1.html')


@app.route('/login2', methods=['POST'])
def login2():
    username = request.form.get('username', '')
    return render_template('login2.html', username=username)


@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        mobile = request.form['mobile']
        # Do something with the user data
        return redirect('/index')
    else:
        username = request.args.get('username', '')  # Get username from query parameters
        return render_template('base.html', username=username)


@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    custom_name = request.form.get('custom_name', '')
    expiration_str = request.form.get('expiration', '')
    expiration_timestamp = datetime.strptime(expiration_str, "%Y-%m-%dT%H:%M")

    if custom_name:
        short_url = f'http://127.0.0.1:5000/{custom_name}'
    else:
        uid = str(uuid.uuid4())[:5]
        short_url = f'http://127.0.0.1:5000/{uid}'

    url_mapping = URLMapping(
        short_url=short_url,
        original_url=url,
        expiration_timestamp=expiration_timestamp
    )

    db.session.add(url_mapping)
    db.session.commit()

    return redirect('/index')


@app.route('/index')
def index():
    url_mapping = URLMapping.query.order_by(URLMapping.id.desc()).first()
    return render_template('index.html', url_mapping=url_mapping)


@app.route('/<uid>')
def redirect_to_url(uid):
    url_mapping = URLMapping.query.filter_by(short_url=f'http://127.0.0.1:5000/{uid}').first()
    if url_mapping and url_mapping.expiration_timestamp >= datetime.now():
        return redirect(url_mapping.original_url)
    else:
        return f'No URL found for {uid}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
