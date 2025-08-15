from pydantic import BaseModel

class inputData(BaseModel):
    text: str

class outputData(BaseModel):
    enhanced_text: str