from fastapi import FastAPI, UploadFile, File
import pdfplumber
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "TERMOSOL HVAC ONLINE"}

# -----------------------------
# UPLOAD PDF
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    models = parse_pdf(path)

    return {
        "message": "file caricato",
        "modelli_trovati": models
    }

# -----------------------------
# PARSER BASE DAIKIN
# -----------------------------
def parse_pdf(path):
    results = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                for line in text.split("\n"):
                    if "RXM" in line or "FTXM" in line or "MXM" in line:
                        results.append(line.split()[0])

    return list(set(results))