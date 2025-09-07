from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, EKS
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.azure.database import SQLDatabases # Replaced PostgreSQL with Azure SQLDatabases for MySQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Pod

with Diagram("AI Legal Mate System", show=False, filename="static/gpt_generated_diagram", direction="LR"):
    # AWS Components (normalized from requirements)
    api_gateway = APIGateway("API Gateway")
    s3_storage = S3("S3 (Document Storage)")
    rds_app_db = RDS("RDS (Application DB)")
    eks_orchestration = EKS("EKS (Kubernetes Orchestration)")
    sagemaker_ml_platform = EC2("SageMaker (ML Platform)") # SageMaker mapped to EC2

    # Generic / Open Source Components (normalized from requirements)
    end_user = Internet("End User")
    user_interface = EC2("User Interface (React/Next.js)") # UserInterface mapped to EC2
    kafka_bus = Kafka("Kafka (Data Ingestion Bus)") # Kafka mapped from synonym
    data_preprocessor = Pod("Data Pre-processing Services") # Generic service hosted by EKS mapped to Pod
    nlp_ai_core = Pod("NLP & AI Core (LLMs, QA)") # Generic service hosted by EKS mapped to Pod
    legal_knowledge_graph = SQLDatabases("Azure MySQL (Legal Knowledge Graph - Neo4j)") # Replaced PostgreSQL with Azure MySQL
    doc_search_index = Dynamodb("Document Search Index") # Elasticsearch mapped to Dynamodb (forbidden to import Elasticsearch module, using closest NoSQL DB)
    doc_gen_review_module = Pod("Document Generation & Review") # Generic service hosted by EKS mapped to Pod
    security_compliance = EC2("Security, Compliance & Audit") # Generic cross-cutting service mapped to EC2
    
    # Monitoring Components
    monitoring_prometheus = Prometheus("Prometheus")
    monitoring_grafana = Grafana("Grafana")
    monitoring_group = [monitoring_prometheus, monitoring_grafana]

    # --- Subgraphs for logical grouping ---
    with Cluster("User Access Layer"):
        end_user >> user_interface
        user_interface >> api_gateway

    with Cluster("Data Ingestion & Storage"):
        s3_storage >> Edge(label="Raw Documents") >> data_preprocessor
        data_preprocessor >> Edge(label="Processed Stream") >> kafka_bus

    with Cluster("AI/ML Core & Compute"):
        kafka_bus >> Edge(label="Training/Updates") >> nlp_ai_core
        data_preprocessor >> Edge(label="Data for Model Training") >> sagemaker_ml_platform
        sagemaker_ml_platform >> Edge(label="Model Deployment") >> nlp_ai_core
        eks_orchestration >> [data_preprocessor, nlp_ai_core, doc_gen_review_module] # EKS hosts these services

    with Cluster("Knowledge & Data Stores"):
        kafka_bus >> Edge(label="Knowledge Updates") >> legal_knowledge_graph
        kafka_bus >> Edge(label="Document Indexing") >> doc_search_index
        rds_app_db

    # --- Core System Flows ---
    api_gateway >> Edge(label="API Requests") >> eks_orchestration

    # NLP & AI Core interactions
    nlp_ai_core >> Edge(label="Context/Retrieval") >> legal_knowledge_graph
    nlp_ai_core >> Edge(label="Semantic Search") >> doc_search_index
    legal_knowledge_graph >> Edge(label="Precedents/Ontology") >> nlp_ai_core

    # Document Generation & Review Module interactions
    doc_gen_review_module - Edge(label="Content Suggestions") - nlp_ai_core
    doc_gen_review_module - Edge(label="Templates/Precedents") - legal_knowledge_graph
    doc_gen_review_module >> Edge(label="Stores Drafts") >> rds_app_db

    # Application data flow
    eks_orchestration >> Edge(label="App Data Read/Write") >> rds_app_db

    # --- Cross-cutting Concerns ---
    api_gateway >> Edge(label="Access Control/Logging") >> security_compliance
    eks_orchestration >> Edge(label="Runtime Security/Audit") >> security_compliance
    rds_app_db >> Edge(label="Data Security") >> security_compliance
    legal_knowledge_graph >> Edge(label="Data Governance") >> security_compliance
    doc_search_index >> Edge(label="Access Control") >> security_compliance

    # Monitoring
    monitoring_group >> eks_orchestration
    monitoring_group >> kafka_bus
    monitoring_group >> s3_storage
    monitoring_group >> rds_app_db
    monitoring_group >> doc_search_index
    monitoring_group >> legal_knowledge_graph