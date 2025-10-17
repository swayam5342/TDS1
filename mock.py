# mock_server.py
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/")
async def root(request: Request):
    body = await request.body()
    print(f"Body: {body.decode(errors='ignore')}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
