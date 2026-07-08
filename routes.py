from flask import Blueprint, jsonify, redirect, render_template, request
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

# edit the issues With a specific id
@api.route("/edit-issue/<int:issue_id>", methods=["GET", "POST"])
def edit_issue(issue_id):

    issue = db.session.get(VulnIssue, issue_id)

    if issue is None:
        return "Issue not found", 404

    if request.method == "POST":

        issue.title = request.form["title"]
        issue.description = request.form["description"]
        issue.severity = request.form["severity"]
        issue.status = request.form["status"]
        issue.reporter = request.form["reporter"]
        issue.assigned_to = request.form["assigned_to"]
        issue.affected_system = request.form["affected_system"]
        issue.cvss_score = float(request.form["cvss_score"])

        db.session.commit()

        return redirect("/issues-page")

    return render_template(
        "edit_issue.html",
        issue=issue
    )
# Update an existing vulnerability issue
@api.route("/issues/<int:issue_id>", methods=["PUT"])
def update_issue(issue_id):

    # Find the issue
    issue = db.session.get(VulnIssue, issue_id)

    if issue is None:
        return jsonify({
            "error": "Issue not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    # Allowed values
    valid_severity = ["Low", "Medium", "High", "Critical"]

    valid_status = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    # Update title
    if "title" in data:
        if not str(data["title"]).strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        issue.title = data["title"]

    # Update description
    if "description" in data:
        if not str(data["description"]).strip():
            return jsonify({"error": "Description cannot be empty"}), 400
        issue.description = data["description"]

    # Update severity
    if "severity" in data:

        if data["severity"] not in valid_severity:
            return jsonify({
                "error": "Severity must be Low, Medium, High or Critical"
            }), 400

        issue.severity = data["severity"]

    # Update status
    if "status" in data:

        if data["status"] not in valid_status:
            return jsonify({
                "error": "Invalid status"
            }), 400

        issue.status = data["status"]

    # Update reporter
    if "reporter" in data:
        issue.reporter = data["reporter"]

    # Update assigned user
    if "assigned_to" in data:
        issue.assigned_to = data["assigned_to"]

    # Update affected system
    if "affected_system" in data:
        issue.affected_system = data["affected_system"]

    # Update CVSS score
    if "cvss_score" in data:
        issue.cvss_score = data["cvss_score"]

    db.session.commit()

    return jsonify({
        "message": "Issue updated successfully",
        "issue": issue.to_dict()
    }), 200

# delete an issue with a specific id
'''@api.route("/issues/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):

  #query the database for the issue with the given id
    issue = db.session.get(VulnIssue, issue_id)

# return an error message if the issue is not found i.e id does not exist in the database
    if issue is None:
        return jsonify({
            "error": "Issue not found"
        }), 404

    db.session.delete(issue)
    db.session.commit()

    return jsonify({
        "message": "Issue deleted successfully"
    }), 200 '''
@api.route("/delete-issue/<int:issue_id>", methods=["GET", "POST"])
def delete_issue_page(issue_id):

    issue = db.session.get(VulnIssue, issue_id)

    if issue is None:
        return f"Issue number not found", 404

    if request.method == "POST":

        db.session.delete(issue)
        db.session.commit()

        return redirect("/issues-page")

    return render_template(
        "delete_issue.html",
        issue=issue
    )

@api.route("/view_issue/<int:issue_id>", methods=["GET"]) #/view_issue/{{ issue.id }}
def view_issue_page(issue_id):

    issue = db.session.get(VulnIssue, issue_id)

    if issue is None:
        return f"Issue number not found", 404

    return render_template(
        "view_issue.html",
        issue=issue
    )


# create a postman test for the API routes. POSTMAN TESTS
# used AI( google overview AI assistant) to generate the postman tests for the API routes, and read through the postman documentation to understand how to use postman to test the API routes.

# api route to render the issues page from template florder
@api.route("/issues-page")
def issues_page():
    search = request.args.get("search", "").strip()

    issues = VulnIssue.query

    if search:
        issues = issues.filter(
            VulnIssue.title.contains(search))

    issues = issues.order_by(
        VulnIssue.created_at.desc()).all()

    return render_template(
        "issues.html",
        issues=issues,
        search=search
    )


# api route to render the create issue page from template folder
@api.route("/create-issue", methods=["GET", "POST"])
def create_issue_page():

    if request.method == "POST":

        issue = VulnIssue(

            title=request.form["title"],

            description=request.form["description"],

            severity=request.form["severity"],

            status=request.form["status"],

            reporter=request.form["reporter"],

            assigned_to=request.form["assigned_to"],

            affected_system=request.form["affected_system"],

            cvss_score=float(request.form["cvss_score"])

        )

        db.session.add(issue)

        db.session.commit()

        return redirect("/issues-page")

    return render_template("create_issue.html")


    #return render_template("create_issue.html")

#api route to render the reports page from template folder
@api.route("/reports")
def reports_page():

    return render_template("report.html")