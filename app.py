from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_names():
    json_path = os.path.join(os.path.dirname(__file__), 'names.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

NAMES_DATABASE = load_names()

@app.route("/", methods=["GET", "POST"])
def index():
    selected_letter = "Ա"
    data = {"male": [], "female": []}
    
    alphabet = list("ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ")

    if request.method == "POST":
        selected_letter = request.form.get("letter", "Ա")

    if selected_letter in NAMES_DATABASE:
        data = NAMES_DATABASE[selected_letter]

    return render_template(
        "index.html", 
        alphabet=alphabet, 
        selected_letter=selected_letter, 
        data=data
    )

if __name__ == "__main__":
    app.run(debug=True)
