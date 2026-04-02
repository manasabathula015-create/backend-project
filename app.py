from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

total = 0
users = {}

@app.route('/')
def home():
    return "Server is running"

@app.route('/submit', methods=['POST'])
def submit():
    global total, users

    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    count = data.get('count')

    # Validation
    if not name or not mobile or count is None:
        return jsonify({"error": "All fields required"}), 400

    if len(str(mobile)) < 10:
        return jsonify({"error": "Enter valid mobile number"}), 400

    try:
        count = int(count)
    except:
        return jsonify({"error": "Count must be a number"}), 400

    # Unique user logic
    if mobile in users:
        users[mobile]["count"] += count
    else:
        users[mobile] = {
            "name": name,
            "count": count
        }

    total += count

    return jsonify({
        "message": "Success",
        "name": users[mobile]["name"],
        "userTotalCount": users[mobile]["count"],
        "totalCount": total
    })

@app.route('/download')
def download():
    file_path = os.path.join(os.getcwd(), "report.csv")

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Mobile", "Count"])

        for mobile, data in users.items():
            writer.writerow([data["name"], mobile, data["count"]])

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
