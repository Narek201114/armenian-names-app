from flask import Flask, render_template, request
import json
import os
from google import genai

app = Flask(__name__)

# Կարգավորում ենք Gemini API-ն (օգտագործում է միջավայրի փոփոխականից կամ ուղղակի բանալին)
# Խորհուրդ է տրվում GEMINI_API_KEY-ը գրանցել համակարգի environment variables-ում
client = genai.Client()

def load_names():
    json_path = os.path.join(os.path.dirname(__file__), 'names.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_names(data):
    json_path = os.path.join(os.path.dirname(__file__), 'names.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
            
            # 2. Եթե բազայում չկա, դիմում ենք Gemini AI-ին
            if not found:
                try:
                    prompt = f"Տուր հայկական «{search_query}» անվան նշանակությունը և սեռը (արական թե իգական)։ Պատասխանը տուր խիստ JSON ձևաչափով հետևյալ կառուցվածքով՝ {{\"name\": \"{search_query}\", \"meaning\": \"նշանակությունը այստեղ\", \"gender\": \"male կամ female\"}}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    # Մաքրում ենք պատասխանը JSON-ի համար
                    text_res = response.text.strip()
                    if text_res.startswith("```json"):
                        text_res = text_res[7:-3].strip()
                    elif text_res.startswith("```"):
                        text_res = text_res[3:-3].strip()
                        
                    ai_data = json.loads(text_res)
                    ai_name = ai_data.get("name", search_query)
                    ai_meaning = ai_data.get("meaning", "Բացատրություն չկա")
                    ai_gender = ai_data.get("gender", "male")
                    
                    # Որոշում ենք առաջին տառը՝ բազայում ավելացնելու համար
                    first_letter = ai_name[0].upper()
                    if first_letter == 'Ա': # պարզեցված ուղղորդում տառերի
                        pass # կամ համապատասխանեցում հայերեն տառերին
                        
                    # Ավելացնում ենք հիշողության և ֆայլի մեջ
                    if first_letter not in NAMES_DATABASE:
                        NAMES_DATABASE[first_letter] = {"male": [], "female": []}
                    if ai_gender not in NAMES_DATABASE[first_letter]:
                        NAMES_DATABASE[first_letter][ai_gender] = []
                        
                    # Ստուգում ենք՝ արդյոք արդեն կա ջնջելու/կրկնելու խուսափելու համար
                    existing_names = [n["name"].lower() for n in NAMES_DATABASE[first_letter][ai_gender]]
                    if ai_name.lower() not in existing_names:
                        NAMES_DATABASE[first_letter][ai_gender].append({"name": ai_name, "meaning": ai_meaning})
                        save_names(NAMES_DATABASE)
                    
                    search_results.append({
                        "name": ai_name,
                        "meaning": ai_meaning,
                        "gender": "Արական" if ai_gender == "male" else "Իգական",
                        "letter": first_letter
                    })
                except Exception as e:
                    # Եթե ԱԲ-ի հարցման ժամանակ խնդիր լինի
                    pass
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
