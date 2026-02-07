import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database with tables"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()

    # Tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_id INTEGER,
                  description TEXT,
                  priority TEXT,
                  due_date TEXT,
                  completed INTEGER DEFAULT 0,
                  created_at TEXT)''')

    # Game state table
    c.execute('''CREATE TABLE IF NOT EXISTS game_state
                 (player1_points INTEGER DEFAULT 0,
                  player2_points INTEGER DEFAULT 0,
                  player1_position INTEGER DEFAULT 0,
                  player2_position INTEGER DEFAULT 0)''')

    # Initialize game state if empty
    c.execute('SELECT * FROM game_state')
    if not c.fetchone():
        c.execute('INSERT INTO game_state VALUES (0, 0, 0, 0)')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def add_task(player_id, description, priority, due_date):
    """Add a task to the database"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (player_id, description, priority, due_date, created_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (player_id, description, priority, due_date, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_tasks(player_id):
    """Get all incomplete tasks for a player"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE player_id = ? AND completed = 0', (player_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    """Mark a task as completed"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_points(player_id, points):
    """Add points to a player"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    column = f"player{player_id}_points"
    c.execute(f'UPDATE game_state SET {column} = {column} + ?', (points,))
    conn.commit()
    conn.close()

def get_game_state():
    """Get current game state"""
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT * FROM game_state')
    state = c.fetchone()
    conn.close()
    return state

# Initialize database when this file is imported
init_db()