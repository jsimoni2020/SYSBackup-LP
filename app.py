from flask import Flask, render_template, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

LOG_FILE = "/app/logs/backup.log"
backup_running = False

def run_backup():
    global backup_running
    backup_running = True
    try:
        source = "/source/"
        dest = "/dest/"
        os.makedirs(dest, exist_ok=True)

        with open(LOG_FILE, "a") as log:
            log.write("========================================\n")
            log.write(f"Backup started via UI\n")

        result = subprocess.run(
            ["rsync", "-av", "--progress", source, dest],
            capture_output=True, text=True
        )

        with open(LOG_FILE, "a") as log:
            log.write(result.stdout)
            if result.stderr:
                log.write("ERRORS:\n" + result.stderr)
            status = "completed successfully" if result.returncode == 0 else f"failed (exit code {result.returncode})"
            log.write(f"Backup {status}\n")
            log.write("========================================\n")
    finally:
        backup_running = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/backup", methods=["POST"])
def start_backup():
    global backup_running
    if backup_running:
        return jsonify({"status": "already_running", "message": "Backup is already in progress."})
    thread = threading.Thread(target=run_backup)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started", "message": "Backup started."})

@app.route("/status")
def status():
    return jsonify({"running": backup_running})

@app.route("/log")
def get_log():
    if not os.path.exists(LOG_FILE):
        return jsonify({"log": "No backup has been run yet."})
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    last_lines = "".join(lines[-200:])
    return jsonify({"log": last_lines})

if __name__ == "__main__":
    os.makedirs("/app/logs", exist_ok=True)
    app.run(host="0.0.0.0", port=51501)
