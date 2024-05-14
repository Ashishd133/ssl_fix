from fastapi import FastAPI, WebSocket
import requests
import json

app = FastAPI()

@app.websocket("/ws_generate")
async def websocket_generate(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        if data == "close":
            await websocket.close()
            break
        
        try:
            request_data = json.loads(data)
            model = request_data.get("model")
            prompt = request_data.get("prompt")
            context = request_data.get("context")
            
            r = requests.post('http://localhost:11434/api/generate',
                              json={
                                  'model': model,
                                  'prompt': prompt,
                                  'context': context,
                              },
                              stream=True)
            print(r)
            r.raise_for_status()

            for line in r.iter_lines():
                body = json.loads(line)
                print(body)
                response_part = body.get('response', '')
                print(response_part)
                print(str(response_part))
                await websocket.send_text(response_part)

                if 'error' in body:
                    raise Exception(body['error'])

                if body.get('done', False):
                    await websocket.send_text(body['context'])
                    break
        except Exception as e:
            await websocket.send_text(str(e))
