
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.database import Dynamodb
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("Simple Blog Platform System", show=False, filename="static/gpt_generated_diagram"):
    user = Internet("User\n(Web Browser)")

    with Cluster("Simple Blog Platform System"):
        frontend = Server("Frontend\n(React.js, HTML/CSS/JS)\n(Client-side UI)")
        backend = Server("Backend\n(Node.js, Express.js)\n(RESTful API)")
        database = Dynamodb("Database\n(MongoDB)\n(NoSQL Document Store)")

        # User interacts directly with the Frontend.
        user >> Edge(label="Interacts via\nHTTP/HTTPS", color="#0056b3", style="bold") >> frontend

        # Frontend communicates with the Backend via RESTful API calls.
        frontend >> Edge(label="RESTful API Calls\n(HTTP/HTTPS, JSON)", color="#28a745", style="bold") >> backend
        backend >> Edge(label="API Responses\n(JSON, Status Codes)", color="#28a745", style="bold") >> frontend

        # Backend performs CRUD operations on the Database.
        backend >> Edge(label="CRUD Operations\n(Mongoose.js)", color="#dc3545", style="bold") >> database
        database >> Edge(label="Data Retrieval/\nStorage Confirmation", color="#dc3545", style="bold") >> backend
