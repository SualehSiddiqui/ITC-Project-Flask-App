import flask
import json
from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

# Global laptops data
laptops = []

def load_laptops():
    """Load laptops from JSON file into global laptops list"""
    global laptops
    with open('data/laptops.json', 'r') as f:
        laptops = json.load(f)

def update_laptops():
    """Update laptops in JSON file from global laptops list"""
    global laptops
    with open('data/laptops.json', 'w') as f:
        json.dump(laptops, f, indent=4)

# Initialize laptops data on startup
load_laptops()

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/laptop')
def edit():
    return render_template('laptop.html')

# ---------------- Laptops Route ----------------
@app.route("/api/laptops", methods=["GET"])
def get_laptops():
    return flask.jsonify(laptops), 200

@app.route("/api/laptops/<int:id>")
def get_laptop_by_id(id):
    for laptop in laptops:
        if laptop['laptopId'] == id:
            return flask.jsonify(laptop)
    return flask.jsonify({"error": "Laptop not found"}), 404

@app.route("/api/laptops/save", methods=['POST'])
def save_laptop():
    new_laptop = request.get_json()
    # Convert laptopId to int for comparison
    new_laptop['laptopId'] = int(new_laptop['laptopId'])
    
    for i, laptop in enumerate(laptops):
        if laptop['laptopId'] == new_laptop['laptopId']:
            laptops[i] = new_laptop
            update_laptops()
            return flask.jsonify({"message": "Laptop updated successfully"}), 200 
            
    return flask.jsonify({"error": "Laptop not found"}), 404


@app.route("/api/laptops/search", methods=['POST'])
def search_laptops():
    criteria = request.get_json()

    search = criteria.get('value', '')


    filtered_laptops = [
        laptop for laptop in laptops
        if (search in laptop['brand'].lower() if search else True)
        or (search in laptop['model'].lower() if search else True)
    ]

    return flask.jsonify(filtered_laptops), 200


if __name__ == "__main__":
    # Development server — use `flask run` or a production server for deployment
    app.run(debug=True, host="0.0.0.0", port=5500)