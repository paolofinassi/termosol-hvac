from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TERMOSOL HVAC - CATALOG ENGINE")

# -----------------------------
# 🧱 CATALOGO STRUTTURATO (BASE REALE)
# -----------------------------
CATALOG = {
    "ue": [
        {"code": "RXM20", "power_kw": 2.0, "type": "mono", "max_ui": 2},
        {"code": "RXM25", "power_kw": 2.5, "type": "mono", "max_ui": 2},
        {"code": "MXM40", "power_kw": 4.0, "type": "multi", "max_ui": 4},
    ],
    "ui": [
        {"code": "FTXM20", "power_kw": 2.0},
        {"code": "FTXM25", "power_kw": 2.5},
        {"code": "FTXM35", "power_kw": 3.5},
    ]
}

# -----------------------------
# 🏠 HOME (INTERFACCIA SEMPLICE)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;padding:30px">
        <h1>TERMOSOL HVAC - CATALOGO TECNICO</h1>

        <h3>Verifica compatibilità</h3>

        <form action="/check" method="get">
            UE:
            <select name="ue">
                <option>RXM20</option>
                <option>RXM25</option>
                <option>MXM40</option>
            </select>

            UI:
            <select name="ui">
                <option>FTXM20</option>
                <option>FTXM25</option>
                <option>FTXM35</option>
            </select>

            Quantità:
            <input type="number" name="qty" value="1" min="1">

            <button type="submit">Verifica</button>
        </form>
    </body>
    </html>
    """

# -----------------------------
# 🔧 ENGINE TECNICO
# -----------------------------
@app.get("/check")
def check(ue: str, ui: str, qty: int = 1):

    ue_data = next((x for x in CATALOG["ue"] if x["code"] == ue), None)
    ui_data = next((x for x in CATALOG["ui"] if x["code"] == ui), None)

    if not ue_data or not ui_data:
        return {"status": "ERROR", "message": "modello non trovato"}

    total_power = ui_data["power_kw"] * qty

    status = "OK"
    issues = []

    # 🔵 regola 1: numero unità
    if qty > ue_data["max_ui"]:
        status = "NO"
        issues.append("Troppi split collegati")

    # 🔵 regola 2: potenza
    if total_power > ue_data["power_kw"] * 1.2:
        status = "WARNING"
        issues.append("Potenza al limite")

    # 🔵 regola 3: mono split
    if ue_data["type"] == "mono" and qty > 1:
        status = "WARNING"
        issues.append("Uso multi su mono unit")

    return {
        "ue": ue,
        "ui": ui,
        "qty": qty,
        "status": status,
        "issues": issues
    }

# -----------------------------
# 📦 EXPORT CATALOGO (FUTURO ENEA)
# -----------------------------
@app.get("/catalog")
def catalog():
    return CATALOG
