import re
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

submissions = []

URL_REGEX = re.compile(
    r'^(https?://)'
    r'([a-zA-Z0-9.-]+)'
    r'(\:[0-9]+)?'
    r'(/.*)?$'
)

# Root route to serve static UI or API status
@app.route('/', methods=['GET'])
def home():
    try:
        return send_from_directory('static', 'index.html')
    except Exception:
        return jsonify({
            "status": "online",
            "message": "DevOps Lab Mid API is running!",
            "endpoints": ["POST /submit", "GET /submissions"]
        }), 200

@app.route('/submit', methods=['POST'])
def submit_assignment():
    data = request.get_json(silent=True) or {}
    
    name = data.get('name')
    reg_number = data.get('reg_number')
    title = data.get('title')
    submission_url = data.get('submission_url')
    
    if not name or not reg_number or not title or not submission_url:
        return jsonify({
            "status": "error",
            "message": "Validation failed: All fields (name, reg_number, title, submission_url) are required."
        }), 400
        
    if not URL_REGEX.match(str(submission_url)):
        return jsonify({
            "status": "error",
            "message": "Validation failed: Invalid submission URL format."
        }), 400
        
    new_submission = {
        "id": len(submissions) + 1,
        "name": name,
        "reg_number": reg_number,
        "title": title,
        "submission_url": submission_url
    }
    submissions.append(new_submission)
    
    return jsonify({
        "status": "success",
        "message": "Submission saved successfully.",
        "data": new_submission
    }), 201

@app.route('/submissions', methods=['GET'])
def get_submissions():
    return jsonify({
        "status": "success",
        "count": len(submissions),
        "submissions": submissions
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)