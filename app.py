import os
import sqlite3
from flask import Flask, request, redirect, url_for, render_template

DB_NAME = os.environ.get("TODO_DB_PATH", "todo.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        checked INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def add_todo(todo_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos(name) VALUES(?)",
        (todo_name,)
    )

    conn.commit()
    conn.close()


def get_todos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, checked FROM todos ORDER BY id DESC")

    todos = cursor.fetchall()

    conn.close()

    return todos




def toggle_todo(todo_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE todos SET checked = CASE checked WHEN 1 THEN 0 ELSE 1 END WHERE id = ?",
        (todo_id,)
    )

    conn.commit()
    conn.close()


def delete_todo_by_id(todo_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

    conn.commit()
    conn.close()


def update_todo(todo_id, todo_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE todos SET name = ? WHERE id = ?",
        (todo_name, todo_id)
    )

    conn.commit()
    conn.close()


app = Flask(__name__)
init_db()


def completed_task(todos):
    count = 0
    for todo in todos:
        if todo["checked"]:
            count += 1
    return count


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if (request.method=="POST"):
        todo_name = request.form.get("todo_name", "").strip()
        if todo_name:
            add_todo(todo_name)

        return redirect(url_for("home"))

    todos = get_todos()
    completed_task_count = completed_task(todos)
    return render_template(
        "index.html",
        items=todos,
        total_task_count=len(todos),
        completed_task_count=completed_task_count
    )


@app.route("/checked/<int:todo_id>", methods=["POST"])
def checkbox(todo_id):
    toggle_todo(todo_id)
    return redirect(url_for('home'))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    delete_todo_by_id(todo_id)
    return redirect(url_for("home"))


@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit_todo(todo_id):
    todo_name = request.form.get("todo_name", "").strip()
    if todo_name:
        update_todo(todo_id, todo_name)
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
