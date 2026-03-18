from flask import Flask, render_template, request, jsonify
from database import init_db, save_hike, get_all_hikes, check_in, get_overdue_hikes
from weather import get_weather
from safety import send_alert
import threading
import time

app = Flask(__name__)
init_db()

def monitor_hikes():
    while True:
        overdue = get_overdue_hikes()
        for hike in overdue:
            hike_id = hike[0]
            location = hike[2]
            emergency_contact = hike[8]
            expected_return = hike[9]
            send_alert(emergency_contact, "Raghav", location, expected_return)
            check_in(hike_id)  # mark as alerted so it doesn't send twice
        time.sleep(60)  # check every 60 seconds

# start background monitor
monitor_thread = threading.Thread(target=monitor_hikes, daemon=True)
monitor_thread.start()

@app.route("/")
def home():
    hikes = get_all_hikes()
    return render_template("index.html", hikes=hikes)

@app.route("/weather", methods=["GET"])
def weather():
    location = request.args.get("location", "Sydney")
    data = get_weather(location)
    return jsonify(data)

@app.route("/log_hike", methods=["POST"])
def log_hike():
    data = request.json
    save_hike(
        data["date"],
        data["location"],
        data["duration"],
        data["distance"],
        data["weather"],
        data["temperature"],
        data["notes"],
        data["emergency_contact"],
        data["expected_return"]
    )
    return jsonify({"status": "saved"})

@app.route("/checkin/<int:hike_id>", methods=["POST"])
def checkin(hike_id):
    check_in(hike_id)
    return jsonify({"status": "checked in"})

@app.route("/hikes", methods=["GET"])
def hikes():
    return jsonify(get_all_hikes())

if __name__ == "__main__":
    app.run(debug=True)