import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.config["CONTACT_EMAIL"] = os.environ.get("CONTACT_EMAIL", "").strip()


@app.get("/")
def home():
    return render_template("index.html", contact_email=app.config["CONTACT_EMAIL"])


@app.get("/healthz")
def health():
    return jsonify(status="healthy"), 200


@app.get("/readyz")
def ready():
    return jsonify(status="ready"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
