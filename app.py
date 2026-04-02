from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

total = 0
today_total = 0

# Structure:
# users = {
#   "mobile": {
#       "name": "User",
#       "dates": {
#           "2026-04-02": 5
#       }
#   }
# }
users = {}

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

@app.route('/')
def home():
    return "Server is running"

@app.route('/submit', methods=['POST'])
def submit():
    global total, today_total, users

    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    count = data.get('count')

    if not name or not mobile or not count:
        return jsonify({"error": "All fields required"}), 400

    count = int(count)
    today = get_today()

    # If user not exists
    if mobile not in users:
        users[mobile] = {
            "name": name,
            "dates": {}
        }

    # If today's entry exists → increase count
    if today in users[mobile]["dates"]:
        users[mobile]["dates"][today] += count
    else:
        users[mobile]["dates"][today] = count

    total += count
    today_total += count

    return jsonify({
        "message": "Count updated",
        "date": today,
        "userTodayCount": users[mobile]["dates"][today],
        "totalCount": total,
        "todayCount": today_total
    })

@app.route('/download')
def download():
    file_path = os.path.join(os.getcwd(), "report.csv")

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Mobile", "Date", "Count"])

        for mobile, data in users.items():
            name = data["name"]
            for date, count in data["dates"].items():
                writer.writerow([name, mobile, date, count])

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
