from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TERMOSOL HVAC - CATALOG ENGINE")

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

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;padding:30px">
        <h1>TERMOSOL HVAC - CATALOGO TECNICO</h1>

        <form action="/check" method="get">
            UE:
            <select name="ue">
                <option>RXM20</option>
                <option>RXM25</option>
                <option>MXM40</option>
            </select>

           
