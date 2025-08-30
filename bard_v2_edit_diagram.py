import pandas as pd
from flask import Flask, render_template, request, jsonify
from bard import call_gemini
from langchain.prompts import PromptTemplate
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
from config import software_design_diagram_code_prompt_template, software_design_diagram_code_prompt_template_test, \
    software_design_requirements_prompt_template, output_template, software_design_diagram_dot_language, \
    modify_code_prompt

app = Flask(__name__)

df = pd.DataFrame(columns=['user_input', 'generated_software_details', 'generated_diagram_code', 'status'])


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
    try:
        subprocess.run(["python", "auto_code_validator.py", code], check=True, capture_output=True, text=True)
        result = subprocess.run(["python", code], check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        status = "correct"

        # Check if diagram file was created
        diagram_path = "static/gpt_generated_diagram.png"
        if not os.path.exists(diagram_path):
            output = "Diagram generation requires Graphviz to be installed. Please install Graphviz from https://graphviz.org/download/ and add it to your system PATH."
            status = "warning"
    except subprocess.CalledProcessError as e:
        error_text = e.stderr.strip()
        if "graphviz.backend.ExecutableNotFound" in error_text or "failed to execute ['dot'" in error_text:
            output = "Diagram generation requires Graphviz to be installed. Please install Graphviz from https://graphviz.org/download/ and add it to your system PATH."
            status = "warning"
        else:
            output = f"Error: {error_text}"
            status = "incorrect"
    except Exception as e:
        output = f"An unexpected error occurred: {e}"
        status = "incorrect"

    return output, status


def append_dict_to_df(df, dict_to_append):
    df = pd.concat([df, pd.DataFrame.from_records([dict_to_append])])
    return df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_and_execute_diagram', methods=['POST'])
def generate_and_execute_diagram():
    user_summary = request.form['user_summary']
    print("User Summary", user_summary)

    # Step 1: Generate Software Requirements Prompt
    generated_design_requirement = generate_software_requirements_prompt(user_summary)

    generated_dot_diagram = generate_dot_language(generated_design_requirement)
    print(generated_dot_diagram)
    # Step 2: Generate Diagram Code Prompt
    generated_diagram_code = generate_diagram_code_prompt(generated_dot_diagram, output_template)
    diagram_code = highlight(generated_diagram_code, PythonLexer(), HtmlFormatter())
    # Step 3: Save and Execute Generated Python Diagram Code
    code_file = save_generated_python_diagram_code(generated_diagram_code)
    execution_result, status = execute_generated_python_diagram_code(code_file)
    print(execution_result)

    # Add the data to the DataFrame
    global df
    df = append_dict_to_df(df, {'user_input': user_summary, 'generated_software_details': generated_design_requirement,
                                'generated_diagram_code': generated_diagram_code, 'status': status})
    df.to_csv('data.csv', mode='a', header=False, index=False)
    return render_template('display.html', generated_design_requirement=generated_design_requirement,
                           generated_diagram_code=diagram_code, python_output="static/gpt_generated_diagram.png",
                           message=execution_result, df=df, id=len(df) - 1)


@app.route('/get_data', methods=['GET'])
def get_data():
    return df.to_json(orient='records')


@app.route('/edit_diagram_code', methods=['GET'])
def edit_diagram_code():
    id = request.args.get('id', 0, type=int)

    # If id is provided, get the specific entry from dataframe
    if id < len(df):
        diagram_code = df.iloc[id]['generated_diagram_code']
    else:
        # If no valid id, use the most recent entry
        if not df.empty:
            diagram_code = df.iloc[-1]['generated_diagram_code']
        else:
            diagram_code = ""

    return render_template('edit_diagram.html', diagram_code=diagram_code, id=id)


@app.route('/save_diagram_code', methods=['POST'])
def save_diagram_code():
    global df
    edit_type = request.form['edit_type']
    id = int(request.form['id'])

    if edit_type == 'manual':
        # Get the manually edited code
        diagram_code = request.form['diagram_code']
    else:  # AI-assisted edit
        # Get the original code and AI instructions
        original_code = request.form['original_code']
        ai_instructions = request.form['ai_instructions']

        # Generate AI-modified code using the instructions
        prompt = f"Modify this diagram code according to these instructions: {ai_instructions}\n\nOriginal code:\n{original_code}"
        diagram_code = call_gemini(prompt)
        # Clean up the response if needed
        diagram_code = diagram_code.replace("```python", "").replace("```", "").strip()

    # Save and execute the modified code
    code_file = save_generated_python_diagram_code(diagram_code)
    execution_result, status = execute_generated_python_diagram_code(code_file)

    # Get the original data
    if id < len(df):
        user_summary = df.iloc[id]['user_input']
        generated_design_requirement = df.iloc[id]['generated_software_details']
    else:
        user_summary = "Custom diagram"
        generated_design_requirement = "Custom diagram created through manual editing"

    # Update the dataframe with the new code
    df = append_dict_to_df(df, {
        'user_input': user_summary,
        'generated_software_details': generated_design_requirement,
        'generated_diagram_code': diagram_code,
        'status': status
    })
    df.to_csv('data.csv', mode='a', header=False, index=False)

    # Format the code for display
    formatted_code = highlight(diagram_code, PythonLexer(), HtmlFormatter())

    return render_template('display.html',
                           generated_design_requirement=generated_design_requirement,
                           generated_diagram_code=formatted_code,
                           python_output="static/gpt_generated_diagram.png",
                           message=execution_result,
                           df=df,
                           id=len(df) - 1)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)