from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

total = 0
today_total = 0
records = []

@app.route('/')
def home():
    return "Server is running"

@app.route('/submit', methods=['POST'])
def submit():
    global total, today_total, records

    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    count = data.get('count')

    if not name or not mobile or not count:
        return jsonify({"error": "All fields required"}), 400

    total += int(count)
    today_total += int(count)

    records.append({
        "name": name,
        "mobile": mobile,
        "count": count
    })

    return jsonify({
        "totalCount": total,
        "todayCount": today_total,
        "individualCount": count
    })

@app.route('/download')
def download():
    file_path = os.path.join(os.getcwd(), "report.csv")

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Mobile", "Count"])

        for r in records:
            writer.writerow([r["name"], r["mobile"], r["count"]])

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
