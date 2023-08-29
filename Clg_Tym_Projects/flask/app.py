from flask import Flask, render_template, request, redirect
import uuid

app = Flask(__name__)

url_mapping = {}

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    custom_name = request.form.get('custom_name', '')
    if custom_name:
        short_url = f'http://127.0.0.1:5000/{custom_name}'
    else:
        uid = str(uuid.uuid4())[:5]
        short_url = f'http://127.0.0.1:5000/{uid}'
    url_mapping[short_url] = url
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html', url_mapping=url_mapping.items())


@app.route('/<uid>')
def redirect_to_url(uid):
    url = url_mapping.get(f'http://127.0.0.1:5000/{uid}')
    if url:
        return redirect(url)
    else:
        return f'No URL found for {uid}'

if __name__ == '__main__':
    app.run(debug=True)
