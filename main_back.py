# Import pysqlite3 first
try:
    import pysqlite3
    version = getattr(pysqlite3, "__version__", "unknown")
    print(f"Successfully imported pysqlite3 version: {version}")
except ImportError as e:
    print(f"Error importing pysqlite3: {e}")
    import sys
    print(f"Python path: {sys.path}")
    print(f"Python executable: {sys.executable}")

import uvicorn
import argparse
import os
from backend.app.routes import create_app
from dotenv import set_key

# Store root_path in environment variable for persistence across reloads
ROOT_PATH = os.environ.get("APP_ROOT_PATH", "")

# Create app with root_path
app = create_app(root_path=ROOT_PATH)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run FastAPI server with custom port")
    parser.add_argument("--port", type=int, default=8090, help="Port number to run the server on")
    parser.add_argument("--root_path", type=str, default="", help="The root path where the API is mounted (e.g., /username/app_name)")
    args = parser.parse_args()

    # Update root path from arguments
    if args.root_path:
        os.environ["APP_ROOT_PATH"] = args.root_path
        # Update app root_path for the initial run
        app.root_path = args.root_path

    print(f"Starting server on port {args.port}")
    print(f"Using root_path: {args.root_path}")

    set_key(".client_env", "BACKEND_PORT", str(args.port))
    set_key(".client_env", "ROOT_PATH", args.root_path)

    uvicorn.run(
        "main_back:app",
        host="0.0.0.0",
        port=args.port,
        root_path=args.root_path,
        reload=True,
        log_level="debug",
        #openapi_url=f"{args.root_path}/openapi.json" if args.root_path else "/openapi.json"
    )
