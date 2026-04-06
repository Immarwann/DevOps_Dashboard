from flask import Flask, render_template
import psutil
import socket
import time

app = Flask(__name__)

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    return f"{hours}h {minutes}m {seconds}s"

@app.route("/")
def dashboard():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    data = {
        "hostname": socket.gethostname(),
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_used": round(memory.used / (1024 ** 3), 2),
        "memory_total": round(memory.total / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_used": round(disk.used / (1024 ** 3), 2),
        "disk_total": round(disk.total / (1024 ** 3), 2),
        "uptime": get_uptime()
    }

    return render_template("index.html", data=data)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
