from fastapi import FastAPI, HTTPException
import uvicorn
import httpx

app = FastAPI()

@app.post("/generate")
async def generate(payload: dict):
    async with httpx.AsyncClient(timeout=60) as client:  # Set timeout to 60 seconds
        try:
            response = await client.post("http://0.0.0.0:11434/api/generate", json=payload)
            response.raise_for_status()
            response=response.json()
            return response['response']
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail="Error communicating with the server") from e
        except httpx.ReadTimeout as e:
            raise HTTPException(status_code=504, detail="Request to the server timed out") from e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,ssl_keyfile="./myclearkey.pem", ssl_certfile="./cert.pem")
