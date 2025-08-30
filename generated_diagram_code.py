
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import APIGateway
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet

with Diagram("E-commerce Microservices", show=False, filename="static/gpt_generated_diagram"):
    client = Internet("React Frontend")
    api_gateway = APIGateway("API Gateway")
    postgresql = PostgreSQL("PostgreSQL DB")
    redis = Redis("Redis Cache")
    kafka = Kafka("Apache Kafka")
    external_payment_gateway = Internet("External Payment Gateway")

    with Cluster("Microservices (Java Spring Boot)"):
        user_svc = Server("User Service")
        product_catalog_svc = Server("Product Catalog Service")
        shopping_cart_svc = Server("Shopping Cart Service")
        order_svc = Server("Order Service")
        payment_svc = Server("Payment Service")
        recommendation_svc = Server("Recommendation Service")
        inventory_svc = Server("Inventory Service")
        search_svc = Server("Search Service") # Elasticsearch connections omitted due to forbidden module

    # 1. User Interaction Flow
    client >> Edge(label="Requests (HTTPS)") >> api_gateway

    # 2. Request Routing (API Gateway to Microservices)
    api_gateway >> Edge(label="/users") >> user_svc
    api_gateway >> Edge(label="/products") >> product_catalog_svc
    api_gateway >> Edge(label="/cart") >> shopping_cart_svc
    api_gateway >> Edge(label="/orders") >> order_svc
    api_gateway >> Edge(label="/payments") >> payment_svc
    api_gateway >> Edge(label="/recommendations") >> recommendation_svc
    api_gateway >> Edge(label="/search") >> search_svc

    # 3. Data Persistence (Microservices to PostgreSQL)
    user_svc >> Edge(label="CRUD User Data") >> postgresql
    product_catalog_svc >> Edge(label="CRUD Product Data") >> postgresql
    shopping_cart_svc >> Edge(label="CRUD Cart Data") >> postgresql
    order_svc >> Edge(label="CRUD Order Data") >> postgresql
    payment_svc >> Edge(label="Store Payment Status") >> postgresql
    recommendation_svc >> Edge(label="Store User Behavior") >> postgresql
    inventory_svc >> Edge(label="Manage Stock Data") >> postgresql

    # 4. Caching (Microservices to Redis)
    user_svc >> Edge(label="Cache User Sessions") >> redis
    product_catalog_svc >> Edge(label="Cache Product Details") >> redis
    shopping_cart_svc >> Edge(label="Cache Cart State") >> redis
    order_svc >> Edge(label="Cache Order Status") >> redis

    # 5. Asynchronous Communication (Microservices via Kafka)
    order_svc >> Edge(label="Publish 'Order Placed' Event") >> kafka
    kafka >> Edge(label="Consume 'Order Placed' (Async Update)") >> inventory_svc
    kafka >> Edge(label="Consume 'Order Placed' (Update User History)") >> recommendation_svc

    # 6. Search Data Flow & 7. Product Search: Omitted due to Elasticsearch being a forbidden component.

    # 8. Payment Processing
    order_svc >> Edge(label="Initiate Payment") >> payment_svc
    payment_svc - Edge(label="Process Payment (PCI DSS)") - external_payment_gateway

    # 9. Synchronous Microservice Interactions
    order_svc >> Edge(label="Check/Reserve Stock") >> inventory_svc
    inventory_svc >> Edge(label="Stock Confirmation") >> order_svc
