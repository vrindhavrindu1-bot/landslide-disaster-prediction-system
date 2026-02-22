from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
app=Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        location TEXT NOT NULL,
        observation TEXT NOT NULL,
        severity TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/submit-report", methods=["POST"])
def submit_report():
    data = request.get_json()
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (user, location, observation, severity) VALUES (?, ?, ?, ?)",
          -       (data["user"], data["location"], data["observation"], data["severity"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Report submitted successfully"})

@app.route("/get-reports", methods=["GET"])
def get_reports():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user, location, observation, severity FROM reports")
    rows = cursor.fetchall()
    conn.close()
    reports = [{"user": r[0], "location": r[1], "observation": r[2], "severity": r[3]} for r in rows]
    return jsonify({"reports": reports})

if __name__ == "__main__":
    app.run(debug=True)

