from flask import   Flask , request , jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/sign-up", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username", "").strip 