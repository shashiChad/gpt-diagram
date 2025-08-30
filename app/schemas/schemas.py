from pydantic import BaseModel

class inputData(BaseModel):
    text: str

class outputData(BaseModel):
    enhanced_text: str

class Input(BaseModel):
    text:str
class Output(BaseModel):
    system_info:str