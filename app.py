from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

# Import converter
from Unicode_KrutiDev_converter import KrutiDev_to_Unicode

app = FastAPI(title="KrutiDev to Unicode API")

@app.get("/")
def home():
    return {"status": "OK"}
    
# CORS (browser se call allow karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "KrutiDev to Unicode API is running"
    }

# 👉 WEBSITE
@app.get("/web", response_class=HTMLResponse)
def web():
    with open("convert.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/convert")
def convert(data: InputText):
    result = KrutiDev_to_Unicode(data.text)
    return {"unicode": result}

@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        return {"error": "PDF se text extract nahi hua (scanned PDF ho sakta hai)"}

    unicode_text = KrutiDev_to_Unicode(text)

    return {
        "unicode": unicode_text
    }
