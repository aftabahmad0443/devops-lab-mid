import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Root endpoint for browser status check
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Local JSON Report Receiver is active and listening for POST requests on /report"
    }), 200

# Report receiver endpoint for GitHub Actions
@app.route('/report', methods=['POST'])
def receive_report():
    try:
        report_data = request.get_json()
        if not report_data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        # Save received report as test-report.json on local computer
        with open('test-report.json', 'w') as f:
            json.dump(report_data, f, indent=4)

        print("\n[+] Test report successfully received and saved to test-report.json")
        return jsonify({"status": "success", "message": "Report saved locally"}), 200

    except Exception as e:
        print(f"[-] Error saving report: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)