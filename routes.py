from flask import Blueprint, jsonify, request
from models import db, VulnIssue

api = Blueprint("api", __name__)

#this route retrieves all vulnerability issues
@api.route("/issues", methods=["GET"])
def get_all_issues():
    #issues = VulnIssue.query.all()
    # sort the issues by the timestamp in descending order 
    issues = VulnIssue.query.order_by(VulnIssue.created_at.desc()).all()

    #return jsonify([issue.to_dict() for issue in issues]), 200
    # return a JSON response with the count of issues and the list of issues
    return jsonify({
    "count": len(issues),
    "issues": [issue.to_dict() for issue in issues]
}), 200

#this route retrieves a specific vulnerability issue by its ID
@api.route("/issues/<int:issue_id>", methods=["GET"])
def get_issue(issue_id):

    issue = VulnIssue.query.get(issue_id)

    if issue is None:
        return jsonify({
            "error": "Issue not found"
        }), 404

    return jsonify(issue.to_dict()), 200

#this route creates a new vulnerability issue
@api.route("/issues", methods=["POST"])
def create_issue():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = [
        "title",
        "description",
        "severity",
        "status",
        "reporter",
        "assigned_to",
        "affected_system"
    ]

    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({"error": f"{field} is required"}), 400

    valid_severity = ["Low", "Medium", "High", "Critical"]

    if data["severity"] not in valid_severity:
        return jsonify({
            "error": "Severity must be Low, Medium, High or Critical"
        }), 400

    valid_status = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if data["status"] not in valid_status:
        return jsonify({
            "error": "Invalid status"
        }), 400

    issue = VulnIssue(
        title=data["title"],
        description=data["description"],
        severity=data["severity"],
        status=data["status"],
        reporter=data["reporter"],
        assigned_to=data["assigned_to"],
        affected_system=data["affected_system"],
        cvss_score=data.get("cvss_score")
    )

    db.session.add(issue)
    db.session.commit()

    return jsonify({
        "message": "Issue created successfully",
        "issue_id": issue.id
    }), 201