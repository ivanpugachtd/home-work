import datetime
from flask import Flask, render_template, request, jsonify


def create_app():
    app = Flask(__name__)
    app.members = []
    app.emails = set()

    @app.route('/')
    def default_route():
        return render_template('index.html', members=app.members)

    @app.route('/member', methods=['POST'])
    def create_member():
        new_member = request.get_json()
        email = new_member.get("email", "")
        name = new_member.get("name", "")

        if not email or not name:
            return jsonify("Error, fields name and email should not be empty".format(email)), 400

        if email in app.emails:
            return jsonify("Error, email = '{}' is already member of the club".format(email)), 400

        new_member['index'] = len(app.members) + 1
        new_member['registration_date'] = datetime.date.today().strftime('%d.%m.%Y')
        app.members.append(new_member)
        app.emails.add(email)

        return jsonify("New member created successfully"), 200

    @app.route('/members', methods=['GET'])
    def get_members():
        return jsonify({"data": app.members})

    return app
