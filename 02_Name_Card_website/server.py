from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from flask import request
from flask import render_template_string





app = Flask(__name__)

# 🔧 Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔌 Initialize the database
db = SQLAlchemy(app)


# creating index route
@app.route("/")
@app.route("/api/cards", methods=["GET"])
def get_cards():
    cards = BusinessCard.query.all()
    return jsonify([card.to_dict() for card in cards]), 200

def home():
    return render_template('index.html')

@app.route("/api/cards", methods=["POST"])
def create_card():
    data = request.get_json()

    # Validate required fields
    required_fields = ["name", "email", "phone", "company", "job_title"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field(s)"}), 400

    # Create new BusinessCard object
    new_card = BusinessCard(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        company=data["company"],
        job_title=data["job_title"]
    )

    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201

@app.route("/api/cards/<int:card_id>", methods=["GET"])
def get_card(card_id):
    card = BusinessCard.query.get(card_id)
    if card:
        return jsonify(card.to_dict()), 200
    else:
        return jsonify({"error": "Card not found"}), 404

@app.route("/api/cards/<int:card_id>", methods=["PUT"])
def update_card(card_id):
    card = BusinessCard.query.get(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    data = request.get_json()

    card.name = data.get("name", card.name)
    card.email = data.get("email", card.email)
    card.phone = data.get("phone", card.phone)
    card.company = data.get("company", card.company)
    card.job_title = data.get("job_title", card.job_title)

    db.session.commit()
    return jsonify(card.to_dict()), 200

@app.route("/api/cards/<int:card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = BusinessCard.query.get(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Card deleted"}), 200


class BusinessCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "job_title": self.job_title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

# Make db accessible when imported
db = db

# Website UI
@app.route("/ui")
def api_ui():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Business Card API</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        input, button { margin: 5px; padding: 5px; }
        .card { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Business Card API Interface</h1>

    <h3>Add New Card</h3>
    <input id="name" placeholder="Name">
    <input id="email" placeholder="Email">
    <input id="phone" placeholder="Phone">
    <input id="company" placeholder="Company">
    <input id="job_title" placeholder="Job Title">
    <button onclick="addCard()">Add</button>

    <h3>All Cards</h3>
    <div id="cards"></div>

    <script>
        async function loadCards() {
            const res = await fetch('/api/cards');
            const cards = await res.json();
            const container = document.getElementById('cards');
            container.innerHTML = '';
            cards.forEach(card => {
                const div = document.createElement('div');
                div.className = 'card';
                div.innerHTML = `
                    <strong>${card.name}</strong> (${card.email})<br>
                    ${card.job_title} at ${card.company}<br>
                    Phone: ${card.phone}<br>
                    <button onclick="deleteCard(${card.id})">Delete</button>
                `;
                container.appendChild(div);
            });
        }

        async function addCard() {
            const data = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                company: document.getElementById('company').value,
                job_title: document.getElementById('job_title').value
            };
            await fetch('/api/cards', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            loadCards();
        }

        async function deleteCard(id) {
            await fetch('/api/cards/' + id, { method: 'DELETE' });
            loadCards();
        }

        loadCards(); // Load cards on page load
    </script>
</body>
</html>
""")

# running the app and setting the required env variable
if __name__ == "__main__":

    # adding the env variable for Flask to work
    # > $env:FLASK_APP = "server"
    import os
    # print(os.environ.get("FLASK_APP"))
    os.environ["FLASK_APP"] = "server"

    # > flask run

    app.run(debug=True)

