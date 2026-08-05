from flask import Flask, render_template, request
import json
import os
from google import genai

app = Flask(__name__)

# Կարգավորում ենք Gemini API-ն
client = genai.Client()

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
    search_query = ""
    search_results = []
    
    alphabet = list("ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ")

    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        
        if search_query:
            query_lower = search_query.lower()
            found = False
            
            # 1. Նախ փնտրում ենք տեղական բազայում
            for letter, categories in NAMES_DATABASE.items():
                for gender in ["male", "female"]:
                    for item in categories.get(gender, []):
                        if query_lower in item["name"].lower():
                            search_results.append({
                                "name": item["name"],
                                "meaning": item["meaning"],
                                "gender": "Արական" if gender == "male" else "Իգական",
                                "letter": letter
                            })
                            found = True
            
            # 2. Եթե բազայում չկա, հարցնում ենք Gemini AI-ին անմիջապես ցուցադրելու համար
            if not found:
                try:
                    prompt = f"Տուր հայկական «{search_query}» անվան նշանակությունը և սեռը (արական թե իգական)։ Պատասխանը տուր խիստ JSON ձևաչափով հետևյալ կառուցվածքով՝ {{\"name\": \"{search_query}\", \"meaning\": \"նշանակությունը այստեղ\", \"gender\": \"male կամ female\"}}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    text_res = response.text.strip()
                    if text_res.startswith("```json"):
                        text_res = text_res[7:-3].strip()
                    elif text_res.startswith("```"):
                        text_res = text_res[3:-3].strip()
                        
                    ai_data = json.loads(text_res)
                    ai_name = ai_data.get("name", search_query)
                    ai_meaning = ai_data.get("meaning", "Բացատրություն չկա")
                    ai_gender = ai_data.get("gender", "male")
                    first_letter = ai_name[0].upper()
                    
                    search_results.append({
                        "name": ai_name,
                        "meaning": ai_meaning,
                        "gender": "Արական" if ai_gender == "male" else "Իգական",
                        "letter": first_letter
                    })
                except Exception as e:
                    print(f"AI Error: {e}") # Կարող եք տեսնել սխալը Logs-ում
        else:
            selected_letter = request.form.get("letter", "Ա")
            if selected_letter in NAMES_DATABASE:
                data = NAMES_DATABASE[selected_letter]
    else:
        if selected_letter in NAMES_DATABASE:
            data = NAMES_DATABASE[selected_letter]

    return render_template(
        "index.html", 
        alphabet=alphabet, 
        selected_letter=selected_letter, 
        data=data,
        search_query=search_query,
        search_results=search_results
    )

if __name__ == "__main__":
    app.run(debug=True)
