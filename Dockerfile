FROM python:3.13

WORKDIR /test

RUN apt-get update && apt-get install -y graphviz

COPY requirement_docker.txt .

RUN pip install -r requirement_docker.txt

COPY generated_diagram_code.py .

CMD [ "python","generated_diagram_code.py" ]