from flask import   Flask , request , jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)

@app.route("/api/sign-up", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username", "").strip 
    password = data.get("password", "").strip
    email    = data.get("email",    "").strip().lower()
    phone_number = data.get("phone_number", "").strip()

    # check for empty fields
    if not all([username, password, email, phone_number]):
        return jsonify({"error": "All fields are required"}), 400
    hashed_password = Bcrypt.generate_password_hash(password).decode("utf-8")
    return jsonify({"message":"Account created"}),200



if __name__ == "__main__":
    app.run(debug=True)

