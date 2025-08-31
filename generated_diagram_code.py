
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.programming.language import Python

with Diagram("Software Design", show=False, filename="static/gpt_generated_diagram", direction="LR"):
    # External User
    user = Internet("User")

    # Frontend Components
    frontend = Server("Frontend\n(React, Tailwind CSS)\nUser Interface")

    # Backend Services Cluster
    with Cluster("Backend Services"):
        backend_api = Server("FastAPI Backend\n(API Server & Controller)")
        langchain_orchestrator = Python("LangChain Orchestrator\n(LLM & DB Integration)")

    # AI Service
    google_gemini = Lambda("Google Gemini\n(LLM Service)")

    # Databases
    vector_database = Dynamodb("Vector Database\n(Embeddings Store)")
    postgresql = PostgreSQL("PostgreSQL\n(Relational DB)")

    # PDF Content Source
    pdf_content = S3("PDF Content\n(Input)")

    # Relationships and Data Flows

    # User Interaction
    user >> Edge(label="Interacts (Browser)") >> frontend
    frontend >> Edge(label="Renders UI") >> user

    # Frontend-Backend Communication
    frontend >> Edge(label="REST API Calls") >> backend_api
    backend_api >> Edge(label="REST API Responses") >> frontend

    # Backend Internal Orchestration
    backend_api >> Edge(label="Routes LLM/DB Tasks") >> langchain_orchestrator
    langchain_orchestrator >> Edge(label="Returns Processed Data") >> backend_api

    # LLM Interaction
    langchain_orchestrator >> Edge(label="LLM API Calls\n(QGen, AnsEval, Embeddings)") >> google_gemini
    google_gemini >> Edge(label="LLM Responses") >> langchain_orchestrator

    # Vector Database Interaction
    langchain_orchestrator >> Edge(label="Query / Write Embeddings") >> vector_database
    vector_database >> Edge(label="Returns Relevant Chunks") >> langchain_orchestrator

    # Relational Database Interaction
    backend_api >> Edge(label="CRUD Operations\n(User, QnA History, PDF Metadata)") >> postgresql
    postgresql >> Edge(label="Data Retrieval") >> backend_api

    # PDF Ingestion & Processing Flow
    pdf_content >> Edge(label="Upload PDF") >> backend_api
    backend_api >> Edge(label="Initiates PDF Processing\n(Text Extraction, Chunking)") >> langchain_orchestrator
    langchain_orchestrator >> Edge(label="Generate Embeddings (for PDF chunks)") >> google_gemini
    langchain_orchestrator >> Edge(label="Store Embeddings (of PDF chunks)") >> vector_database
