from flask import Flask, Response, render_template, request, stream_with_context
import time

app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/timer')
def timer_page():
    return render_template('timer.html')


if __name__ == '__main__':
    app.run(debug=True)