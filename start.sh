#!/bin/bash

# Source environment variables from .client_env
source .client_env

# Function to check and kill process on a port
kill_process_on_port() {
    PORT=$1
    echo "Checking port $PORT..."
    
    # Find process using the port
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        PID=$(lsof -i :$PORT -t)
    else
        # Linux
        PID=$(netstat -tulpn 2>/dev/null | grep ":$PORT " | awk '{print $7}' | cut -d'/' -f1)
    fi
    
    if [ -z "$PID" ]; then
        echo "No process found using port $PORT"
    else
        echo "Found process $PID using port $PORT. Killing it..."
        kill -9 $PID
        echo "Process killed"
    fi
}

# Check and free ports before starting
echo "Checking and freeing ports before starting services..."

# Kill process on frontend port
if [ ! -z "$FRONTEND_PORT" ]; then
    kill_process_on_port $FRONTEND_PORT
fi

# Kill process on backend port
if [ ! -z "$BACKEND_PORT" ]; then
    kill_process_on_port $BACKEND_PORT
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the backend service
echo "Starting backend on port $BACKEND_PORT..."
python main_back.py --port $BACKEND_PORT > logs/backend.log &

# Start the frontend service
echo "Starting frontend on port $FRONTEND_PORT..."
streamlit run main_front.py --server.port=$FRONTEND_PORT > logs/frontend.log &

echo "Services started:"
echo "- Backend running on $BASE_URL:$BACKEND_PORT"
echo "- Frontend running on $BASE_URL:$FRONTEND_PORT"
echo "- Using RAG API at $RAG_API_ENDPOINT"
echo "Log files are in the logs directory"