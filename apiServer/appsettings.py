APP_PROTOCOL= "tcp"

# Socket facing clients
FRONTEND_SOCKET=dict(
    proto = APP_PROTOCOL,
    addr="127.0.0.1",
    port= "7000"
)

# Socket facing services
SERVICE_SOCKET=dict(
    proto = APP_PROTOCOL,    
    addr="127.0.0.1",
    port= "6000"
)

WORKER_SERVICES_COUNT = 2

# Mongo connections #
DB_SERVER="localhost"
DB_PORT="27017"
DB_NAME="testdb"
DB_COLLECTION="entities"