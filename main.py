from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# Create the database tables within the application context
with app.app_context():
    db.create_all()

@app.route('/api/entries', methods=['POST'])
def create_entry():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({"error": "Name is required"}), 400

    entry = Entry(name=data['name'], description=data.get('description'))
    db.session.add(entry)
    db.session.commit()

    return jsonify(entry.to_dict()), 201

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    db.session.delete(entry)
    db.session.commit()

    return jsonify({"message": "Entry deleted"}), 200

@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = Entry.query.all()
    return jsonify([entry.to_dict() for entry in entries]), 200

if __name__ == '__main__':
    app.run(debug=True)
