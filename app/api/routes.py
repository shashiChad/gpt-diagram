from fastapi import APIRouter
from app.schemas.schemas import inputData,outputData
import app.services.enhancer_service as es
from app.schemas.enhancer_prompt import PROMPT_TEMPLATE
from google.genai import types

router = APIRouter()

@router.get("/")
def root():
    return {"message":"hello from server"}
@router.post("/enhancer",response_model=outputData)
def enhance(txt:inputData):
    raw_text= txt.text
    content = PROMPT_TEMPLATE.format(text = raw_text)
    response = es.client.models.generate_content(
        model = es.model,
        contents= content,
        config = types.GenerateContentConfig(
            temperature = 0
        )

    )
    new_text = response.text
    return {"enhanced_text":new_text}
