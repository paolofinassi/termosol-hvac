from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TERMOSOL HVAC - INTERFACE")

# -----------------------------
# DATI CATALOGO (SEMPLIFICATO MA REALISTICO)
# -----------------------------
UE_MODELS = {
    "RXM20": {"power": 2.0},
    "RXM25": {"power": 2.5},
    "MXM40": {"power": 4.0},
}

UI_MODELS = {
    "FTXM20": {"power": 2.0},
    "FTXM25": {"power": 2.5},
    "FTXM35": {"power": 3.5},
}

# -----------------------------
# HOME (INTERFACCIA VERA)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>TERMOSOL HVAC</title>
    </head>
    <body style="font-family: Arial; padding: 30px;">
        <h1>TERMOSOL HVAC - CONFIGURATORE</h1>

        <h3>Test compatibilità</h3>

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
            <input type="number" name="qty_ui" value="1" min="1">

            <button type="submit">Verifica</button>
        </form>
    </body>
    </html>
    """

# -----------------------------
# LOGICA TECNICA
# -----------------------------
@app.get("/check")
def check(ue: str, ui: str, qty_ui: int = 1):

    ue_data = UE_MODELS.get(ue)
    ui_data = UI_MODELS.get(ui)

    if not ue_data or not ui_data:
        return {"error": "modello non trovato"}

    total_ui = ui_data["power"] * qty_ui

    status = "OK"
    issues = []

    if qty_ui > 2:
        status = "NO"
        issues.append("Troppi split collegati")

    if total_ui > ue_data["power"] * 1.2:
        status = "WARNING"
        issues.append("Potenza al limite")

    return {
        "ue": ue,
        "ui": ui,
        "qty": qty_ui,
        "status": status,
        "issues": issues
    }
