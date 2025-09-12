## Apis

# Enhancer ---------------
@router.post("/enhancer",response_model=outputData)
* string input { text: str}
* string output { enhanced_text: str }

* Enhancer button on clicking will replace the prompt with new one on the prompt box

# Generate diagram code -----------------
@router.post('/generate_diagram_code',response_model=Output)

* string input from input box { text:str }
* string output -- code { diagram_code:str }

* On clicking submit button near the prompt box ,it will take user input and provide code which needs to be shown on the editable terminal on new page redirected to .

# Saving the generated code ---------------
@router.post('/terminal_save', response_model=Exeedit)

* string input --- code { diagram:str }
* string output ---code { "messg": "diagram saved" }----for confirmation

* On clicking save button the code generated on terminal will get saved to "generated_diagram_code.py"

Note:- The terminal is editable,so user can edit and also press save to save the new code

# Executing the diagram code --------------------
@router.get('/execute_diagram',response_model=ExeDia)

* string output --- diagram path { "diagram": r"static\gpt_generated_diagram.png" }

* On clicking execute button ,the diagram code file "generated_diagram_code.py" will run and the diagram generated will be saved in "static\gpt_generated_diagram.png"

# Editing diagram with prompt -------------------------
@router.post('/edit_code',response_model=Exeedit)

* string input -- prompt from a seperate prompt box which will appear after the diagram is generated { diagram:str }
* string output -- code which will get displayed in terminal { messg:str }

* After than save process save -> execute


## Example---------

# For enhancer ------
** input
{
  "text": "Generate a system design for a blog platform"
}
** output
{
  "enhanced_text": "Design a comprehensive system for a modern blog platform, utilizing a microservices architecture with Node.js and Express for backend services, React for the frontend, and PostgreSQL as the primary database. The design should encompass user management (authentication, authorization), content creation and management (posts, comments, categories), media storage, and search functionality. Prioritize scalability to handle a growing number of users and posts, ensure high availability and fault tolerance, implement robust data security measures, and optimize for performance and maintainability, considering deployment strategies on a cloud platform like AWS."
}

# For generate diagram ----------

** input
{
  "text": "Design a comprehensive system for a modern blog platform, utilizing a microservices architecture with Node.js and Express for backend services, React for the frontend, and PostgreSQL as the primary database. The design should encompass user management (authentication, authorization), content creation and management (posts, comments, categories), media storage, and search functionality. Prioritize scalability to handle a growing number of users and posts, ensure high availability and fault tolerance, implement robust data security measures, and optimize for performance and maintainability, considering deployment strategies on a cloud platform like AWS."
}
**output
{
  "diagram_code": "\nfrom diagrams import Diagram, Cluster, Edge\nfrom diagrams.aws.database import RDS\nfrom diagrams.aws.network import APIGateway\nfrom diagrams.aws.storage import S3\nfrom diagrams.onprem.monitoring import Grafana, Prometheus\nfrom diagrams.onprem.network import Internet\nfrom diagrams.k8s.compute import Pod\n\nwith Diagram(\"Software Design\", show=False, filename=\"static/gpt_generated_diagram\"):\n    # Frontend Application\n    frontend_app = Internet(\"Frontend Application\\n(React)\")\n\n    with Cluster(\"AWS Cloud Environment\"):\n        api_gw = APIGateway(\"API Gateway\")\n\n        with Cluster(\"Microservices (AWS EKS)\"):\n            user_service = Pod(\"User Service\")\n            post_service = Pod(\"Post Service\")\n            comment_service = Pod(\"Comment Service\")\n            category_tag_service = Pod(\"Category/Tag Service\")\n            media_service = Pod(\"Media Service\")\n            search_service = Pod(\"Search Service\")\n\n        # Databases and Storage\n        rds_db = RDS(\"Primary Database\\n(PostgreSQL)\")\n        s3_storage = S3(\"Media Storage\")\n        # OpenSearch is omitted as it's not in the allowed imports list and has no direct synonym.\n\n        with Cluster(\"Monitoring & Observability\"):\n            # CloudWatch is omitted as it's a forbidden import.\n            prometheus_monitor = Prometheus(\"Prometheus\")\n            grafana_dashboard = Grafana(\"Grafana\")\n\n    # --- Relationships ---\n\n    # Frontend to API Gateway\n    frontend_app >> Edge(label=\"Client Requests\") >> api_gw\n\n    # API Gateway to Microservices\n    api_gw >> Edge(label=\"User APIs\") >> user_service\n    api_gw >> Edge(label=\"Post APIs\") >> post_service\n    api_gw >> Edge(label=\"Comment APIs\") >> comment_service\n    api_gw >> Edge(label=\"Category/Tag APIs\") >> category_tag_service\n    api_gw >> Edge(label=\"Media APIs\") >> media_service\n    api_gw >> Edge(label=\"Search APIs\") >> search_service\n\n    # Microservices to Databases/Storage\n    user_service >> Edge(label=\"User Data CRUD\") >> rds_db\n    post_service >> Edge(label=\"Post Data CRUD\") >> rds_db\n    comment_service >> Edge(label=\"Comment Data CRUD\") >> rds_db\n    category_tag_service >> Edge(label=\"Category/Tag Data CRUD\") >> rds_db\n    media_service >> Edge(label=\"Store/Retrieve Media Files\") >> s3_storage\n    media_service >> Edge(label=\"Media Metadata CRUD\") >> rds_db\n\n    # Search Service Interactions (OpenSearch omitted, so related edges are adjusted)\n    # SearchService -> OpenSearch [label=\"Index & Query\"]; is omitted.\n    post_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    comment_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    category_tag_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    user_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n\n    # Monitoring Relationships (CloudWatch omitted)\n    microservices = [user_service, post_service, comment_service, category_tag_service, media_service, search_service]\n    # {microservices} -> CloudWatch [label=\"Logs & Metrics\", style=dotted]; is omitted.\n    microservices >> Edge(label=\"Metrics Scraping\", style=\"dotted\") >> prometheus_monitor\n    prometheus_monitor >> Edge(label=\"Visualize Metrics\") >> grafana_dashboard\n    # CloudWatch -> Grafana [label=\"Dashboarding\", style=dotted]; is omitted.\n"
}

# For terminal save------------

** input
{
  "diagram": "\nfrom diagrams import Diagram, Cluster, Edge\nfrom diagrams.aws.database import RDS\nfrom diagrams.aws.network import APIGateway\nfrom diagrams.aws.storage import S3\nfrom diagrams.onprem.monitoring import Grafana, Prometheus\nfrom diagrams.onprem.network import Internet\nfrom diagrams.k8s.compute import Pod\n\nwith Diagram(\"Software Design\", show=False, filename=\"static/gpt_generated_diagram\"):\n    # Frontend Application\n    frontend_app = Internet(\"Frontend Application\\n(React)\")\n\n    with Cluster(\"AWS Cloud Environment\"):\n        api_gw = APIGateway(\"API Gateway\")\n\n        with Cluster(\"Microservices (AWS EKS)\"):\n            user_service = Pod(\"User Service\")\n            post_service = Pod(\"Post Service\")\n            comment_service = Pod(\"Comment Service\")\n            category_tag_service = Pod(\"Category/Tag Service\")\n            media_service = Pod(\"Media Service\")\n            search_service = Pod(\"Search Service\")\n\n        # Databases and Storage\n        rds_db = RDS(\"Primary Database\\n(PostgreSQL)\")\n        s3_storage = S3(\"Media Storage\")\n        # OpenSearch is omitted as it's not in the allowed imports list and has no direct synonym.\n\n        with Cluster(\"Monitoring & Observability\"):\n            # CloudWatch is omitted as it's a forbidden import.\n            prometheus_monitor = Prometheus(\"Prometheus\")\n            grafana_dashboard = Grafana(\"Grafana\")\n\n    # --- Relationships ---\n\n    # Frontend to API Gateway\n    frontend_app >> Edge(label=\"Client Requests\") >> api_gw\n\n    # API Gateway to Microservices\n    api_gw >> Edge(label=\"User APIs\") >> user_service\n    api_gw >> Edge(label=\"Post APIs\") >> post_service\n    api_gw >> Edge(label=\"Comment APIs\") >> comment_service\n    api_gw >> Edge(label=\"Category/Tag APIs\") >> category_tag_service\n    api_gw >> Edge(label=\"Media APIs\") >> media_service\n    api_gw >> Edge(label=\"Search APIs\") >> search_service\n\n    # Microservices to Databases/Storage\n    user_service >> Edge(label=\"User Data CRUD\") >> rds_db\n    post_service >> Edge(label=\"Post Data CRUD\") >> rds_db\n    comment_service >> Edge(label=\"Comment Data CRUD\") >> rds_db\n    category_tag_service >> Edge(label=\"Category/Tag Data CRUD\") >> rds_db\n    media_service >> Edge(label=\"Store/Retrieve Media Files\") >> s3_storage\n    media_service >> Edge(label=\"Media Metadata CRUD\") >> rds_db\n\n    # Search Service Interactions (OpenSearch omitted, so related edges are adjusted)\n    # SearchService -> OpenSearch [label=\"Index & Query\"]; is omitted.\n    post_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    comment_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    category_tag_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    user_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n\n    # Monitoring Relationships (CloudWatch omitted)\n    microservices = [user_service, post_service, comment_service, category_tag_service, media_service, search_service]\n    # {microservices} -> CloudWatch [label=\"Logs & Metrics\", style=dotted]; is omitted.\n    microservices >> Edge(label=\"Metrics Scraping\", style=\"dotted\") >> prometheus_monitor\n    prometheus_monitor >> Edge(label=\"Visualize Metrics\") >> grafana_dashboard\n    # CloudWatch -> Grafana [label=\"Dashboarding\", style=dotted]; is omitted.\n"
}
** output

get saved to file

# For Execute diagram -------

** no input direct image generation
** output
{
  "diagram": "static\\gpt_generated_diagram.png"
}

# For Edit Diagram ------------

** input
{
  "diagram": "Add mysql database and add react for frontend"
}
** output
{
  "messg": "from diagrams import Diagram, Cluster, Edge\nfrom diagrams.aws.database import RDS\nfrom diagrams.aws.network import APIGateway\nfrom diagrams.aws.storage import S3\nfrom diagrams.onprem.monitoring import Grafana, Prometheus\nfrom diagrams.k8s.compute import Pod\nfrom diagrams.onprem.database import Mysql\nfrom diagrams.programming.framework import React\n\nwith Diagram(\"Software Design\", show=False, filename=\"static/gpt_generated_diagram\"):\n    # Frontend Application\n    frontend_app = React(\"Frontend Application\")\n\n    with Cluster(\"AWS Cloud Environment\"):\n        api_gw = APIGateway(\"API Gateway\")\n\n        with Cluster(\"Microservices (AWS EKS)\"):\n            user_service = Pod(\"User Service\")\n            post_service = Pod(\"Post Service\")\n            comment_service = Pod(\"Comment Service\")\n            category_tag_service = Pod(\"Category/Tag Service\")\n            media_service = Pod(\"Media Service\")\n            search_service = Pod(\"Search Service\")\n\n        # Databases and Storage\n        rds_db = RDS(\"Primary Database\\n(PostgreSQL)\")\n        mysql_db = Mysql(\"MySQL Database\")\n        s3_storage = S3(\"Media Storage\")\n        # OpenSearch is omitted as it's not in the allowed imports list and has no direct synonym.\n\n        with Cluster(\"Monitoring & Observability\"):\n            # CloudWatch is omitted as it's a forbidden import.\n            prometheus_monitor = Prometheus(\"Prometheus\")\n            grafana_dashboard = Grafana(\"Grafana\")\n\n    # --- Relationships ---\n\n    # Frontend to API Gateway\n    frontend_app >> Edge(label=\"Client Requests\") >> api_gw\n\n    # API Gateway to Microservices\n    api_gw >> Edge(label=\"User APIs\") >> user_service\n    api_gw >> Edge(label=\"Post APIs\") >> post_service\n    api_gw >> Edge(label=\"Comment APIs\") >> comment_service\n    api_gw >> Edge(label=\"Category/Tag APIs\") >> category_tag_service\n    api_gw >> Edge(label=\"Media APIs\") >> media_service\n    api_gw >> Edge(label=\"Search APIs\") >> search_service\n\n    # Microservices to Databases/Storage\n    user_service >> Edge(label=\"User Data CRUD\") >> rds_db\n    post_service >> Edge(label=\"Post Data CRUD\") >> rds_db\n    comment_service >> Edge(label=\"Comment Data CRUD\") >> rds_db\n    category_tag_service >> Edge(label=\"Category/Tag Data CRUD\") >> rds_db\n    media_service >> Edge(label=\"Store/Retrieve Media Files\") >> s3_storage\n    media_service >> Edge(label=\"Media Metadata CRUD\") >> rds_db\n    # MySQL database is added but no specific connections are defined by the user for it.\n\n    # Search Service Interactions (OpenSearch omitted, so related edges are adjusted)\n    # SearchService -> OpenSearch [label=\"Index & Query\"]; is omitted.\n    post_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    comment_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    category_tag_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n    user_service >> Edge(label=\"Index Data (Async)\", style=\"dashed\") >> search_service\n\n    # Monitoring Relationships (CloudWatch omitted)\n    microservices = [user_service, post_service, comment_service, category_tag_service, media_service, search_service]\n    # {microservices} -> CloudWatch [label=\"Logs & Metrics\", style=dotted]; is omitted.\n    microservices >> Edge(label=\"Metrics Scraping\", style=\"dotted\") >> prometheus_monitor\n    prometheus_monitor >> Edge(label=\"Visualize Metrics\") >> grafana_dashboard\n    # CloudWatch -> Grafana [label=\"Dashboarding\", style=dotted]; is omitted."
}