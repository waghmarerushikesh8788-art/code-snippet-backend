from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import init_extensions
from routes.auth import auth_bp
from routes.snippet import snippet_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

init_extensions(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(snippet_bp, url_prefix="/api/snippet")

@app.route("/")
def home():
    return jsonify({"message": "Backend is running"})

if __name__ == "__main__":
    app.run(debug=True)
