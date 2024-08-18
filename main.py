from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
import sqlite3
import pytz
import csv
import os

########################### database #########################
def create_database():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard (
        name TEXT,
        score TEXT,
        topic TEXT,
        date_time TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_database()
########################### database #########################

app = Flask(__name__)

################################## quiz ########################################
correct_answers = {
    'question0': 'B',
    'question1': 'B',
    'question2': 'D',
    'question3': 'A',
    'question4': 'B',
    'question5': 'C',
    'question6': 'C',
    'question7': 'A',
    'question8': 'D',
    'question9': 'A',
    'question10': 'A',
    'question11': 'B',
    'question12': 'D',
}

def calculate_score(answers):
    score = 0
    for question, answer in answers.items():
        if correct_answers.get(question) == answer:
            score += 1
    return score

def store_score(name, topic, score):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    sg_timezone = pytz.timezone('Asia/Singapore')
    date_time = datetime.now(sg_timezone).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO leaderboard (name, score, topic, date_time)
    VALUES (?, ?, ?, ?)
    ''', (name, score, topic, date_time))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name, score, topic, date_time
    FROM leaderboard
    ORDER BY score DESC, topic ASC
    ''')
    leaderboard = cursor.fetchall()
    conn.close()
    return leaderboard

@app.route('/leaderboard')
def leaderboard():
    leaderboard = get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)
################################## quiz ########################################

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/standard_curves', methods=['GET', 'POST'])
def standard_curves():
    if request.method == 'POST':
        answers = {key: value for key, value in request.form.items() if key.startswith('question')}
        score = calculate_score(answers)
        name = request.form['name']
        topic = "Standard Curves"
        store_score(name, topic, score)
        return redirect('/leaderboard')
    else:
        return render_template("standard_curves.html")
        
@app.route('/differentiation', methods=['GET', 'POST'])
def differentiation():
    if request.method == 'POST':
        answers = {key: value for key, value in request.form.items() if key.startswith('question')}
        score = calculate_score(answers)
        name = request.form['name']
        topic = "Differentiation + AOD"
        store_score(name, topic, score)
        return redirect('/leaderboard')
    else:
        return render_template("differentiation.html")

@app.route('/integration', methods=['GET', 'POST'])
def integration():
    if request.method == 'POST':
        answers = {key: value for key, value in request.form.items() if key.startswith('question')}
        score = calculate_score(answers)
        name = request.form['name']
        topic = "Integration"
        store_score(name, topic, score)
        return redirect('/leaderboard')
    else:
        return render_template("integration.html")

@app.route('/add', methods=['POST'])
def add():
    message = request.form['message']
    sg_timezone = pytz.timezone('Asia/Singapore')
    date_time = datetime.now(sg_timezone).strftime("%Y-%m-%d %H:%M:%S")
    new_message = [date_time, message]

    # file closes after with block
    try:
        with open("message.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(new_message)
    except Exception as e:
        print(f"Error: {e}")

    return redirect('/forum')

@app.route('/forum')
def forum():
    messages = []
    if os.path.exists('message.csv'):
        with open('message.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                messages.append(row)
    return render_template("forum.html", messages=messages)


@app.route('/home', methods=['POST'])
def return_home():
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
