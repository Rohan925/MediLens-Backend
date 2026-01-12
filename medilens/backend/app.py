from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

# Core config
from core.config import settings

# Services
from services.ocr_service import extract_text_from_image
from services.drug_name_extractor import extract_drug_name

# -------------------------------------------------
# FastAPI app
# -------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

# -------------------------------------------------
# CORS (frontend access)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
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
# OCR API
# -------------------------------------------------

@app.post("/api/ocr")
async def ocr_image(file: UploadFile = File(...)):
    temp_path = None

    try:
        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # Run OCR
        extracted_text = extract_text_from_image(temp_path)

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the image",
            )

        # Extract drug name from OCR text
        drug_name = extract_drug_name(extracted_text)

        return {
            "success": True,
            "drug_name": drug_name,
            "raw_text": extracted_text,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}",
        )

    finally:
        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
