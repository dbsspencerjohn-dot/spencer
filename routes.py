from flask import Blueprint, jsonify, request
from models import db, Issue

api = Blueprint("api", __name__)


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

    issue = Issue(
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