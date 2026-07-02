from flask import Blueprint, jsonify, request
from spencer.models import vulnIssue, db

api = Blueprint('api', __name__)

@api.route('/api/issues', methods=['POST'])
def create_issue():

    data = request.get_json()
    
    #print(data)
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    required_fields = ['title', 'description', 'severity', 'status', 'reporter', 'assigned_to', 'affected_system']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Create a new vulnerability issue
    issue = VulnIssue(
        title=data['title'],
        description=data['description'],
        severity=data['severity'],
        status=data['status'],
        reporter=data['reporter'],
        assigned_to=data['assigned_to'],
        affected_system=data['affected_system']
    )

    db.session.add(issue)
    db.session.commit()

    return jsonify({"message": "Issue created successfully"}), 201