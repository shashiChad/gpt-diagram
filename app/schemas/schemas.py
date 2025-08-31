from pydantic import BaseModel

class inputData(BaseModel):
    text: str

class outputData(BaseModel):
    enhanced_text: str

class Input(BaseModel):
    text:str
class Output(BaseModel):
    system_info:str
    diagram_code:str
class ExeDia(BaseModel):
    msg:str
class EditDia(BaseModel):
    diagram:str
class Exeedit(BaseModel):
    messg:str