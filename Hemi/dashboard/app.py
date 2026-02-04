from flask import Flask, render_template, jsonify
from dashboard.data_store import get_data

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/traffic-data")
def traffic_data():
    congestion, emergency_count = get_data()

    if len(congestion) == 0:
        level = "LOW"
        avg = 0
    else:
        avg = sum(congestion) / len(congestion)
        if avg < 10:
            level = "LOW"
        elif avg < 20:
            level = "MEDIUM"
        else:
            level = "HIGH"

    return jsonify({
        "congestion_history": congestion,
        "average_congestion": round(avg, 2),
        "congestion_level": level,
        "emergency_count": emergency_count
    })

if __name__ == "__main__":
    app.run(debug=True)
