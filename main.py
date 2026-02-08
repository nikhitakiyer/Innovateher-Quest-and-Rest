from flask import Flask, render_template, request, jsonify
import random
from database import add_task, get_tasks, complete_task, update_points, get_game_state

app = Flask(__name__)

#Variables

#Lists
active_list = ["take a 15 minute walk outside, do 30 jumping jacks, stretch for 10 minutes, Watch a funny video for 5 minutes, Eat a healthy snack"]

print("Quest & Rest Game Starting...")

# Home page - shows intro screen
@app.route('/')
def home():
    return render_template('index.html')

# Player setup page
@app.route('/setup')
def setup():
    return render_template('setup.html')

#Tasks Page
@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')
# Game page
@app.route('/game')
def game():
    return render_template('game.html')

#API: Add a task
@app.route('/api/add_task', methods=['POST'])
def api_add_task():
    data = request.json
    add_task(data['player_id'], data['description'], data['priority'], data['due_date'])
    return jsonify({"status": "success"})

# API: Get tasks
@app.route('/api/get_tasks/<int:player_id>')
def api_get_tasks(player_id):
    tasks = get_tasks(player_id)
    return jsonify({"tasks": tasks})

# API: Complete task
@app.route('/api/complete_task/<int:task_id>', methods=['POST'])
def api_complete_task(task_id):
    complete_task(task_id)
    return jsonify({"status": "success"})

# API: Update points
@app.route('/api/update_points', methods=['POST'])
def api_update_points():
    data = request.json
    update_points(data['player_id'], data['points'])
    return jsonify({"status": "success"})

# Winner page
@app.route('/winner')
def winner():
    return render_template('winner.html')

# Rules page
@app.route('/rules')
def rules():
    return render_template('rules.html')

if __name__ == '__main__':
    print("Quest & Rest Game Starting...")
    app.run(host='0.0.0.0', port=8080, debug=True)

