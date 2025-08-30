# =========================
# config.py (FINAL - error free)
# =========================

software_design_requirements_prompt_template = """As an expert in writing software design details, use below summary to provide template with below points:

User Summary: {user_summary}

Software Design Template:
1. **Overview:**
   - Provide a high-level overview of the software design.

2. **Components:**
   - Identify and describe the key components of the system.

3. **Entities:**
   - Extract entities such as libraries, packages, cloud tools, frameworks, etc., mentioned in the summary.

4. **Relationships:**
   - Illustrate the relationships between the identified components.

5. **Context:**
   - Extract the contextual information related to the software design based on the user's summary.

6. **Technology Stack:**
   - Specify the technologies and tools that will be used in the software design.

Note: Please provide the above details in about 500 words."""

# ---------- DOT Normalization Template ----------
software_design_diagram_dot_language = """As an expert in understanding software design requirements and creating diagrams, please use the
{generated_design_requirement} to generate a diagram in DOT language.

- Prefer the following normalized component names to ease code generation later:
  * AWS/API Gateway -> APIGateway
  * AWS/CloudFront -> CloudFront
  * AWS/Kinesis -> Kinesis
  * AWS/SQS -> SQS
  * AWS/SNS -> SNS
  * AWS/S3 -> S3
  * AWS/RDS -> RDS
  * AWS/EKS -> EKS
  * OnPrem/Spark -> Spark
  * OnPrem/Kafka -> Kafka
  * OnPrem/Redis -> Redis
  * OnPrem/PostgreSQL -> PostgreSQL
  * OnPrem/Mysql -> Mysql
  * OnPrem/Server -> Server
  * Monitoring/Prometheus -> Prometheus
  * Monitoring/Grafana -> Grafana
- Avoid introducing components outside this list unless strictly necessary; if you must, map them to the closest equivalent."""

# ---------- Allowed Imports (VALID in diagrams v0.24.4) ----------
_ALLOWED_IMPORT_MAP = """
Allowed imports (module -> classes):

AWS:
- diagrams.aws.network -> APIGateway, CloudFront, VPC, ELB, Route53
- diagrams.aws.analytics -> Kinesis
- diagrams.aws.integration -> SNS, SQS
- diagrams.aws.storage -> S3
- diagrams.aws.compute -> EC2, Lambda, EKS
- diagrams.aws.database -> RDS, Dynamodb

GCP:
- diagrams.gcp.compute -> GCE
- diagrams.gcp.database -> Bigtable
- diagrams.gcp.network -> VPN

Azure:
- diagrams.azure.compute -> VM

On-Prem:
- diagrams.onprem.compute -> Server
- diagrams.onprem.database -> Mysql, PostgreSQL
- diagrams.onprem.queue -> Kafka
- diagrams.onprem.analytics -> Spark
- diagrams.onprem.inmemory -> Redis
- diagrams.onprem.monitoring -> Grafana, Prometheus
- diagrams.onprem.network -> Internet, Nginx

Generic / Programming / K8s:
- diagrams.programming.language -> Python, Go
- diagrams.k8s.compute -> Pod
- diagrams.k8s.infra -> Node
"""

# ---------- Forbid invalid imports ----------
_FORBIDDEN_IMPORTS = """
Forbidden (do NOT import from these modules or names in v0.24.4):
- diagrams.azure.database.*, diagrams.azure.integration.*, diagrams.azure.network.*
- diagrams.aws.apigateway, diagrams.aws.cdn, diagrams.aws.mobile, diagrams.aws.monitoring.Cloudwatch*
- diagrams.generic.os.*, diagrams.generic.blank.Cylinder
- Any Elastic/Elasticsearch modules (Elastic, elastic.*)
- Any CloudWatch alias not under a valid module
"""

# ---------- Synonym Map ----------
_SYNONYM_MAP = """
Name normalization (if DOT or requirement mentions these, map to the allowed classes):
- "API Gateway" or "api-gateway" -> APIGateway (aws.network)
- "CDN" -> CloudFront (aws.network)
- "Kinesis stream/streams/analytics" -> Kinesis (aws.analytics)
- "Queue" or "message queue" -> SQS (aws.integration)
- "Topic", "pub/sub", "event bus" -> SNS (aws.integration)
- "Object storage", "bucket" -> S3 (aws.storage)
- "Relational DB", "MySQL on AWS", "SQL Database", "Azure SQL" -> RDS (aws.database)
- "Kubernetes on AWS" -> EKS (aws.compute)
- "Cache", "in-memory store" -> Redis (onprem.inmemory)
- "Stream processor", "batch/ETL engine" -> Spark (onprem.analytics)
- "Message broker", "RabbitMQ" -> Kafka (onprem.queue)
- "App server", "service" -> Server (onprem.compute)
"""

# ---------- Code Prompt Template ----------
software_design_diagram_code_prompt_template = f"""
As an expert in writing diagram code using the Diagrams Python library (version 0.24.4), generate the complete diagram code for the following software design requirement.

Strict constraints (MUST follow):
- Use ONLY classes from the allowed import map below. Do not invent modules or classes.
- Never import from forbidden modules listed below.
- Apply the synonym map to normalize component names to allowed classes.
- Start your output with the **canonical import block** shown below, but keep only the lines you actually use.
- Use 'with Diagram(...)' (without 'as diagram') and set show=False, filename="gpt_generated_diagram".
- Connect nodes using '-' or '>>' (do NOT use add_edge).
- Output ONLY Python code.

{_ALLOWED_IMPORT_MAP}
{_FORBIDDEN_IMPORTS}
{_SYNONYM_MAP}

Canonical import block (copy this, then delete unused lines):
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda, EKS
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.analytics import Kinesis
from diagrams.aws.network import VPC, APIGateway, CloudFront, ELB, Route53
from diagrams.aws.storage import S3
from diagrams.gcp.compute import GCE
from diagrams.gcp.database import Bigtable
from diagrams.gcp.network import VPN
from diagrams.azure.compute import VM
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mysql, PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Internet, Nginx
from diagrams.programming.language import Python, Go
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node

Input requirement (DOT-derived summary allowed):
{{generated_dot_diagram}}

Instructions:
1) Normalize any component names per the synonym map before choosing a class.
2) If a component is not in the allowed map, select the closest allowed equivalent or omit it—NEVER add new imports.
3) Do not import from forbidden modules.
4) Ensure every imported class is actually instantiated and used in the diagram.
5) Use clear labels on nodes and set show=False, filename="gpt_generated_diagram".
6) Output only valid Python code, no prose.

Store only python code in below template format:
{{output_template}}
"""

software_design_diagram_code_prompt_template_test = software_design_diagram_code_prompt_template.replace(
    "filename=\"gpt_generated_diagram\"", "filename=\"static/gpt_generated_diagram\""
)

output_template = '''generated diagram code'''

modify_code_prompt = """
As an expert in fixing Python diagrams code for version 0.24.4, examine the error and rewrite ONLY the necessary parts to satisfy these rules:
- Replace any invalid or forbidden imports with the closest valid class from the allowed import map.
- Do NOT introduce new modules beyond the allowed map.
- Keep show=False and filename unchanged.
- Ensure the final code runs without import errors.

Original Code:
{code}

Error:
{error_message}
"""
