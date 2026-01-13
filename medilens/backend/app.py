from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import traceback

# Core config
from core.config import settings

# Services
from services.ocr_service import extract_text_from_image
from services.drug_name_extractor import extract_drug_names
from services.openfda_service import fetch_drug_info

# -------------------------------------------------
# FastAPI app
# -------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health check
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }

# -------------------------------------------------
# OCR → Drug Extraction → OpenFDA
# -------------------------------------------------

@app.post("/api/ocr")
async def ocr_image(file: UploadFile = File(...)):
    temp_path = None

    try:
        # 1️⃣ Save uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # 2️⃣ OCR
        extracted_text = extract_text_from_image(temp_path)

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the image"
            )

        # 3️⃣ LEVEL‑3 drug name extraction (dynamic)
        drug_names = extract_drug_names(extracted_text)

        # 4️⃣ OpenFDA lookup (for each drug)
        drug_info = []
        for drug in drug_names:
            info = fetch_drug_info(drug)
            if info:
                drug_info.append(info)

        # 5️⃣ Response
        return {
            "success": True,
            "drug_names": drug_names,
            "drug_info": drug_info,
            "raw_text": extracted_text,
        }

    except Exception as e:
        # 🔥 IMPORTANT: show real error in terminal
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="OCR processing failed"
        )

    finally:
        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
