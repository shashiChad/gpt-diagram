from fastapi import APIRouter
from app.schemas.schemas import inputData,outputData,Input,Output,ExeDia
import app.services.enhancer_service as es
from app.schemas.enhancer_prompt import PROMPT_TEMPLATE
from google.genai import types
# -------------------new import---------------------------

from app.bard import call_gemini
from langchain.prompts import PromptTemplate
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
from app.design_prompt import software_design_diagram_code_prompt_template, software_design_diagram_code_prompt_template_test,software_design_requirements_prompt_template, output_template, software_design_diagram_dot_language,modify_code_prompt

# --------------------end--------------------------------

router = APIRouter()

# ---------------------functions--------------------------

def generate_software_requirements_prompt(user_summary):
    prompt = PromptTemplate(template=software_design_requirements_prompt_template, input_variables=['user_summary'])
    prompt_formatted_str = prompt.format(user_summary=user_summary)
    generated_output = call_gemini(prompt_formatted_str)
    return generated_output

def generate_dot_language(generated_design_requirement):
    prompt = PromptTemplate(template=software_design_diagram_dot_language,
                            input_variables=['generated_design_requirement'])
    prompt_formatted_str = prompt.format(generated_design_requirement=generated_design_requirement)
    generated_dot_output = call_gemini(prompt_formatted_str)
    generated_dot_code = generated_dot_output.replace("dot", "")
    generated_dot_code = generated_dot_code.replace("```", "")
    return generated_dot_output

def generate_diagram_code_prompt(generated_dot_diagram, output_template):
    prompt = PromptTemplate(template=software_design_diagram_code_prompt_template_test,
                            input_variables=['generated_dot_diagram', 'output_template'])
    prompt_formatted_str = prompt.format(generated_dot_diagram=generated_dot_diagram, output_template=output_template)
    generated_diagram_code = call_gemini(prompt_formatted_str)
    generated_diagram_code = generated_diagram_code.replace("python", "")
    generated_diagram_code = generated_diagram_code.replace("```", "")
    return generated_diagram_code

def modify_code(code, error_message):
    prompt = PromptTemplate(template=modify_code_prompt, input_variables=['code', 'error_message'])
    prompt_formatted_str = prompt.format(code=code, error_message=error_message)
    generated_diagram_code = call_gemini(prompt_formatted_str)
    generated_diagram_code = generated_diagram_code.replace("python", "")
    generated_diagram_code = generated_diagram_code.replace("```", "")
    return generated_diagram_code

def save_generated_python_diagram_code(generated_diagram_code):
    # clean_code = generated_diagram_code.replace("python", "")
    file_path = "generated_diagram_code.py"
    with open(file_path, 'w') as file:
        file.write(generated_diagram_code)
    return file_path

def execute_generated_python_diagram_code(code):
    subprocess.run(["python",code])
# ---------------------end--------------------------------
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

@router.post('/generate_diagram',response_model=Output)
def generate_sysinfo_and_diagram(txt:Input):
    data=txt.text
    software_requirements=generate_software_requirements_prompt(data)
    generated_dot_diagram = generate_dot_language(software_requirements)
    generated_diagram_code = generate_diagram_code_prompt(generated_dot_diagram, output_template)
    # diagram_code = highlight(generated_diagram_code, PythonLexer(), HtmlFormatter())

    save_generated_python_diagram_code(generated_diagram_code)

    return Output(
        system_info=software_requirements,
        diagram_code=generated_diagram_code
    )

@router.get('/execute_diagram',response_model=ExeDia)
def execute_diagram():
    execute_generated_python_diagram_code("generated_diagram_code.py")
    return {"msg": "hello from server"}


