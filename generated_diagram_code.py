
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Pod

with Diagram("E-Commerce Design", show=False, filename="static/gpt_generated_diagram", direction="LR"):
    # External Components
    client = Internet("User Clients\n(Web/Mobile)")
    external_payment_gateway = Server("External Payment\nGateway")

    with Cluster("Edge Infrastructure"):
        api_gateway = APIGateway("API Gateway")
        cloudfront = CloudFront("CDN (CloudFront)")
        s3 = S3("S3 (Static Assets/Logs)")

    with Cluster("Deployment & Orchestration"):
        with Cluster("Kubernetes Cluster (EKS)") as cluster_eks_node:
            eks_cluster = EKS("Kubernetes Cluster (EKS)") # Explicit EKS node
            with Cluster("Core Microservices"):
                user_service = Pod("User Service")
                product_catalog_service = Pod("Product Catalog Service")
                cart_service = Pod("Cart Service")
                order_service = Pod("Order Service")
                payment_service = Pod("Payment Service")
                search_service = Pod("Search Service")
                recommendation_engine = Pod("Recommendation Engine")
                notification_service = Pod("Notification Service")
                admin_service = Pod("Admin Service")

    with Cluster("Data Stores"):
        rds = RDS("Relational DB (RDS)")
        redis = Redis("Redis (Cache)")
        # Elasticsearch is omitted as it is not in the allowed imports and has no direct equivalent.

    with Cluster("Messaging & Event Bus"):
        kafka = Kafka("Kafka (Message Broker)")

    with Cluster("Observability"):
        prometheus = Prometheus("Prometheus (Monitoring)")
        grafana = Grafana("Grafana (Dashboards)")

    # Relationships

    # Client Interactions
    client >> Edge(label="Static Content Fetch") >> cloudfront
    client >> Edge(label="API Requests (HTTP/S)") >> api_gateway

    # Edge Infrastructure Routing to Services
    api_gateway >> Edge(label="Routes API") >> [
        user_service,
        product_catalog_service,
        cart_service,
        order_service,
        search_service,
        admin_service
    ]

    # Service to Data Store Interactions
    user_service >> Edge(label="Reads/Writes User Data") >> rds
    product_catalog_service >> Edge(label="Reads/Writes Product Data") >> rds
    cart_service >> Edge(label="Reads/Writes Cart Data") >> rds
    order_service >> Edge(label="Reads/Writes Order Data") >> rds

    # ProductCatalogService -> Elasticsearch (omitted)
    # SearchService -> Elasticsearch (omitted)

    user_service >> Edge(label="Caches User Sessions") >> redis
    product_catalog_service >> Edge(label="Caches Product Details") >> redis
    cart_service >> Edge(label="Caches Cart State") >> redis
    recommendation_engine >> Edge(label="Caches Recommendations") >> redis

    # Synchronous Service-to-Service Communication (RESTful APIs)
    cart_service >> Edge(label="Get Product Details") >> product_catalog_service
    order_service >> Edge(label="Clear Cart after Order") >> cart_service
    order_service >> Edge(label="Request Payment Processing") >> payment_service
    payment_service >> Edge(label="Integrates With") >> external_payment_gateway

    admin_service >> Edge(label="Manage Users") >> user_service
    admin_service >> Edge(label="Manage Products") >> product_catalog_service
    admin_service >> Edge(label="Manage Orders") >> order_service

    # Asynchronous Service-to-Service Communication (Kafka)
    order_service >> Edge(label="Publishes 'Order Placed' Event") >> kafka
    kafka >> Edge(label="Consumes Order Events") >> notification_service

    product_catalog_service >> Edge(label="Publishes Product Change Events") >> kafka
    kafka >> Edge(label="Consumes Product Changes") >> recommendation_engine
    kafka >> Edge(label="Consumes Product Changes\n(for re-indexing)") >> search_service # Retained, SearchService itself handles it

    user_service >> Edge(label="Publishes User Activity Events") >> kafka
    cart_service >> Edge(label="Publishes Cart Activity Events") >> kafka
    kafka >> Edge(label="Consumes User/Cart Activity") >> recommendation_engine

    # Recommendation Engine Specific
    recommendation_engine >> Edge(label="Reads Behavioral/Product Data") >> rds

    # Observability
    [
        user_service,
        product_catalog_service,
        cart_service,
        order_service,
        payment_service,
        search_service,
        recommendation_engine,
        notification_service,
        admin_service
    ] >> Edge(label="Exposes Metrics") >> prometheus
    prometheus >> Edge(label="Scrapes & Visualizes Metrics") >> grafana
