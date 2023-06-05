import uvicorn
from server.core.application import create_app


our_app = create_app()

if __name__ == "__main__":
    uvicorn.run(our_app, host = '0.0.0.0', port = '8000')