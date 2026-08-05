from flask import Flask, render_template, request

app = Flask(__name__)

# Բազա՝ ըստ հայոց այբուբենի տառերի (օրինակների հիման վրա կարող եք ընդլայնել)
NAMES_DATABASE = {
    "Ա": {
        "male": [
            {"name": "Արամ", "meaning": "Վսեմ, բարձր, հանգիստ, ազնիվ"},
            {"name": "Արթուր", "meaning": "Արջի կամ արևի զորություն, քաջ, հզոր"},
            {"name": "Աշոտ", "meaning": "Հույս, հենարան, երջանիկ"},
            {"name": "Արմեն", "meaning": "Արիական, հայկական, մարտիկ"}
        ],
        "female": [
            {"name": "Անի", "meaning": "Գեղեցիկ, շքեղ, հին հայկական մայրաքաղաքի անունից"},
            {"name": "Անահիտ", "meaning": "Անբողջական, մաքուր, բարոյապես մաքուր (դիցանուն)"},
            {"name": "Աստղիկ", "meaning": "Փոքրիկ աստղ, սիրո և գեղեցկության դիցուհի"},
            {"name": "Արփի", "meaning": "Արև, արևի շող"}
        ]
    },
    "Բ": {
        "male": [
            {"name": "Բաբկեն", "meaning": "Պապիկ, հայրական, նախնի"},
            {"name": "Բագրատ", "meaning": "Աստծո պարգև, տրված Աստծուց"}
        ],
        "female": [
            {"name": "Բեատրիս", "meaning": "Երջանկություն բերող, երջանիկ"},
            {"name": "Բավական", "meaning": "Բավական է (կիրառվում է որպես հայկական ավանդական անուն)"}
        ]
    },
    "Գ": {
        "male": [
            {"name": "Գևորգ", "meaning": "Հողագործ, երկրագործ"},
            {"name": "Գրիգոր", "meaning": "Արթուն, հսկող"},
            {"name": "Գարեգին", "meaning": "Գարնանային, լուսավոր"}
        ],
        "female": [
            {"name": "Գայանե", "meaning": "Երկրային, հողային (կամ հունարենից՝ հանգիստ, խաղաղ)"},
            {"name": "Գոհար", "meaning": "Թանկարժեք քար, ակն, ականջօղ"}
        ]
    },
    "Դ": {
        "male": [
            {"name": "Դավիթ", "meaning": "Սիրելի, սիրված"},
            {"name": "Դանիել", "meaning": "Աստված իմ դատավորն է"}
        ],
        "female": [
            {"name": "Դիանա", "meaning": "Աստվածային, լուսավոր (դիցանուն)"},
            {"name": "Դայանա", "meaning": "Ողորմած, հզոր"}
        ]
    }
    # Այբուբենի մյուս տառերը կարող եք շարունակել այս նույն տրամաբանությամբ
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_letter = "Ա"
    data = {"male": [], "female": []}
    
    # Հայոց այբուբենի բոլոր տառերի ցանկը ընտրության համար
    alphabet = list("ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ")

    if request.method == "POST":
        selected_letter = request.form.get("letter", "Ա")
        if selected_letter in NAMES_DATABASE:
            data = NAMES_DATABASE[selected_letter]

    return render_template("index.html", alphabet=alphabet, selected_letter=selected_letter, data=data)

if __name__ == "__main__":
    app.run(debug=True)
