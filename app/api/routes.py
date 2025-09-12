from fastapi import APIRouter,Body
from app.schemas.schemas import inputData,outputData,Input,Output,ExeDia,EditDia,Exeedit,Action
import app.services.enhancer_service as es
from app.schemas.enhancer_prompt import PROMPT_TEMPLATE
from google.genai import types
# -------------------new import---------------------------
import codecs
from app.bard import call_gemini
from langchain.prompts import PromptTemplate
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
from app.design_prompt import software_design_diagram_code_prompt_template, software_design_diagram_code_prompt_template_test,software_design_requirements_prompt_template, output_template, software_design_diagram_dot_language,modify_code_prompt
# ----------------terminal edit import----------------------------
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

from app.schemas.edit_diagram_code import TEMPLATE_DIAGRAM_EDIT
# --------------------end--------------------------------
# from fastapi.middleware.cors import CORSMiddleware
router = APIRouter()
search= GoogleSerperAPIWrapper()

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
# ---------docker execution--------------------
def execute_docker():
    build_command = ["docker", "build", "-t","diagramgpt", "."]
    subprocess.run(build_command)
    run_command = ["docker", "run", "-v","./static:/test/static","diagramgpt"]
    subprocess.run(run_command)

def write_string_to_file(filename, content):
    with open(filename, 'w') as file: #encoding='utf-8'
        file.write(content.strip())
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
        # system_info=software_requirements,
        diagram_code=generated_diagram_code
    )

@router.get('/execute_diagram',response_model=ExeDia)
def execute_diagram():
    execute_docker()
    return {"diagram": r"static\gpt_generated_diagram.png"}
# ----------------------------------------------------------------------------------------------------------------------
# have so dockerize it to make secure
# @router.post('/edit_and_execute',response_model=Exeedit)
# def edit_and_execute(diagram_code:str=Body(...)):
#     # diagram_code=inp.diagram
#     cleaned_diagram_code = diagram_code.replace('\u00A0', ' ')
#     final_formatted_code = codecs.decode(cleaned_diagram_code, 'unicode_escape')
#     write_string_to_file("generated_diagram_code.py",final_formatted_code)
#     execute_generated_python_diagram_code("generated_diagram_code.py")
#     return {"messg": "diagram generated"}

@router.post('/terminal_save', response_model=Exeedit)
def terminal_save(inp: EditDia):
    diagram_code = inp.diagram
    write_string_to_file("generated_diagram_code.py", diagram_code)

    # execute_generated_python_diagram_code("generated_diagram_code.py")
    return {"messg": "diagram saved"}

# @router.post('/edit_code', response_model=Exeedit)
# def edit_code(inp:EditDia):
#     with open('generated_diagram_code.py', 'r') as f:
#         code_content = f.read()
#     user_input = inp
#     prompt = PromptTemplate.from_template(TEMPLATE_DIAGRAM_EDIT)
#     llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
#     parser = StrOutputParser()
#     chain = prompt | llm | parser
#     response = chain.invoke({
#         "user_input": user_input,
#         "diagram_code": code_content
#     })
#     # write_string_to_file('generated_diagram_code.py', response)
#     return {"messg": response}

# ------------------------testing using agentic workflow--------------------------------

@router.post('/edit_code',response_model=Exeedit)
def edit_code(inp:EditDia):
    with open('generated_diagram_code.py', 'r') as f:
        code_content = f.read()
    user_input = inp
    # ----------------------------------------------------------------------------
    LLM=ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature=0)
    prmpt=PromptTemplate.from_template(
        """
            You are an expert at analyzing user requests about software architecture diagrams. Extract the user's intent and the specific technologies they mention.If the user want to modify or replace i.e, want to change one with other,then take the technologies only he want to add or introducing and keep intent as modify for that.For delete use delete
            {user_request}
        """
    )
    chn=prmpt|LLM.with_structured_output(Action)

    result=chn.invoke({'user_request':user_input})

    if result.intent.upper() in ["ADD","MODIFY"]:
        # print(result.technologies)
        result1=[]
        target_site = "diagrams.mingrammer.com"
        for tech in result.technologies:
            search_query = f' from {tech} site:- {target_site}'
            result1.append(search.run(search_query))
        search_result="\n\n".join(result1)
        print(search_result)
    else:
        search_result="No new info required"
    # -----------------------------------------------------------------------------
    prompt = PromptTemplate.from_template(TEMPLATE_DIAGRAM_EDIT)
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
    parser = StrOutputParser()
    chain = prompt | llm | parser
    response = chain.invoke({
        "user_input": user_input,
        "diagram_code": code_content,
        "search_content": search_result
    })
    return {"messg": response}