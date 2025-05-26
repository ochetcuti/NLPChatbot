"""
server.py: server initalisation file loading blueprints
"""
from flask import Flask, Blueprint, render_template, request, jsonify
from scripted.routes import scripted_blueprint
from semantic.routes import semantic_blueprint
from nltk_setup_packages import install_nltk_resources

app = Flask(__name__)
install_nltk_resources()
# both modules under different URL prefixes
app.register_blueprint(scripted_blueprint, url_prefix="/scripted")
app.register_blueprint(semantic_blueprint, url_prefix="/semantic")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
