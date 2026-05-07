from fastapi import FastAPI

app = FastAPI(title="TERMOSOL HVAC - TECH ENGINE")

UE_MODELS = {
    "RXM20": {"power_kw": 2.0, "phase": "mono", "max_ui": 2},
    "RXM25": {"power_kw": 2.5, "phase": "mono", "max_ui": 2},
    "MXM40": {"power_kw": 4.0, "phase": "multi", "max_ui": 4},
}

UI_MODELS = {
    "FTXM20": {"power_kw": 2.0},
    "FTXM25": {"power_kw": 2.5},
    "FTXM35": {"power_kw": 3.5},
}

@app.get("/")
def home():
    return {"status": "TECH ENGINE ONLINE"}

@app.get("/check")
def check(ue: str, ui: str, qty_ui: int = 1):

    ue_data = UE_MODELS.get(ue)
    ui_data = UI_MODELS.get(ui)

    if not ue_data or not ui_data:
        return {"status": "ERROR", "message": "modello non trovato"}

    result = {
        "ue": ue,
        "ui": ui,
        "qty_ui": qty_ui,
        "status": "OK",
        "issues": []
    }

    total_ui_power = ui_data["power_kw"] * qty_ui

    if qty_ui > ue_data["max_ui"]:
        result["status"] = "NO"
        result["issues"].append("Too many indoor units")

    if total_ui_power > ue_data["power_kw"] * 1.2:
        result["status"] = "WARNING"
        result["issues"].append("Power borderline")

    if ue_data["phase"] == "mono" and qty_ui > 1:
        result["status"] = "WARNING"
        result["issues"].append("Mono unit with multiple indoor")

    return result
