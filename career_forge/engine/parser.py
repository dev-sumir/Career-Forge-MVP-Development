# career_forge/engine/parser.py

import io
import spacy
from docx import Document
from pydantic import BaseModel, Field
from pypdf import PdfReader
from spacy.tokens import Doc

# --- A small setup note ---
# To make this code run, you'll need to install spaCy and its English model.
# Run these commands in your terminal:
# pip install spacy
# python -m spacy download en_core_web_sm

# Load the spaCy AI model. We do this once when the module is loaded.
# This model is lightweight and powerful for understanding text structure.
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    NLP = None


class ParsedResume(BaseModel):
    """
    This is our high-end output. Instead of just text, we create a structured
    object that includes the raw text AND the processed AI document ('doc' object).
    This 'doc' object is incredibly powerful for the next steps.
    """
    raw_text: str = Field(description="The complete, unmodified text from the resume.")
    doc: Doc = Field(description="The resume text processed by the spaCy NLP model.")

    class Config:
        # Pydantic needs this to handle custom types like the spaCy Doc object.
        arbitrary_types_allowed = True


def parse_resume(file_content: bytes, content_type: str) -> ParsedResume:
    """
    The main parsing function. It takes the raw file, extracts text, and then
    uses the spaCy AI model to process it into a structured format.
    """
    raw_text = ""
    if content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(file_content))
            raw_text = "".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            # In a real system, you'd log this error.
            raw_text = ""  # Return empty text on failure

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            doc = Document(io.BytesIO(file_content))
            raw_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            raw_text = ""  # Return empty text on failure

    else:
        # For simplicity, we'll only handle PDF and DOCX for now.
        raise ValueError(f"Unsupported file type for AI parsing: {content_type}")

    # This is the key AI step. We take the raw text and process it.
    # The NLP model breaks the text into tokens, sentences, and adds
    # linguistic features (like parts of speech) that we can use later.
    if NLP and raw_text:
        processed_doc = NLP(raw_text)
    else:
        # Handle cases where spaCy isn't loaded or text is empty
        processed_doc = NLP("") if NLP else None

    return ParsedResume(raw_text=raw_text, doc=processed_doc)