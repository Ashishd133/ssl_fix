import os
import json
import logging
from fastapi import FastAPI, HTTPException,WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from agent import AgentObj
from generate_uuid import generate_uuid
from time_stamp import time_now
from dotenv import load_dotenv
load_dotenv()
import requests

app = FastAPI()

class NegotiateModel(BaseModel):
    model_name: str


@app.post("/negotiate")
def negotiate(model_data: NegotiateModel):
    """
    POST method for negotiating chat models and generating tokens.

    Returns:
        str: JSON-formatted token or an error message.
    """
    try:
        AgentObj.periodic_disconnect_agent()
        user_id = time_now() + generate_uuid()
        model_name = model_data.model_name
        

        if not model_name:
            raise HTTPException(status_code=400, detail="Enter a valid model name")
        AgentObj.add_agent(user_id,model_name)
        base_url = os.environ.get("WEBAPP_BASE_URL")
        if base_url is None:
            raise ValueError("Base URL is missing.")       
        return {
            "baseUrl": base_url,
            "token": user_id,
            "url": base_url + "ws/access_token=" + user_id
            }
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")
    
connections = {}


@app.websocket("/ws_generate/{user_id}")
async def websocket_generate(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket  # Store WebSocket connection with user_id
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if data == "close":
                await websocket.close()
                del connections[user_id]  # Remove WebSocket connection on close
                break

            try:
                session_id = message.get("access_token")
                agent_obj = AgentObj
                model = agent_obj.get_agent(session_id)
                prompt = message.get("prompt")
                context = message.get("context")
                # print("I am here now", model,prompt,context)

                r = requests.post('http://localhost:11434/api/generate',
                                  json={
                                      'model': model,
                                      'prompt': prompt,
                                      'context': context,
                                  },
                                  stream=True)
                r.raise_for_status()

                for line in r.iter_lines():
                    body = json.loads(line)
                    response_part = body.get('response', '')
                    await websocket.send_text(response_part)

                    if 'error' in body:
                        raise Exception(body['error'])

                    if body.get('done', False):
                        await websocket.send_text(body['context'])
                        break
            except Exception as e:
                await websocket.send_text(str(e))
    except WebSocketDisconnect:
        del connections[user_id]  # Remove WebSocket connection on disconnect

async def send_to_user(user_id: str, message: str):
    if user_id in connections:
        websocket = connections[user_id]
        await websocket.send_text(message)
    else:
        # Handle case when user is not connected
        # For example, you could log a message or perform other actions
        print(f"User {user_id} is not connected.")
