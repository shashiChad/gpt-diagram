from pydantic import BaseModel
from  typing import List

class inputData(BaseModel):
    text: str

class outputData(BaseModel):
    enhanced_text: str

class Input(BaseModel):
    text:str
class Output(BaseModel):
    # system_info:str
    diagram_code:str
class ExeDia(BaseModel):
    diagram:str
class EditDia(BaseModel):
    diagram:str
class Exeedit(BaseModel):
    messg:str
# ------------------------------------------------------------------------
class Action(BaseModel):
    intent:str
    technologies:List[str]