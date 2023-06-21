import uvicorn
from server.core.application import create_app

app = create_app()

@app.get("/hello")
def hello():
    return "hellow world"

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = '8000')