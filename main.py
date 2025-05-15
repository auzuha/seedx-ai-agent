from fastapi import FastAPI

from fastapi.responses import StreamingResponse

from utils.graph import a as agent


from models.models import QueryRequest

app = FastAPI()



@app.post('/query')
async def query(q: QueryRequest):
    resp = agent.get_bot_response(q.query, q.history)
    print(resp)
    return {'resp': resp}

@app.post('/stream')
async def stream(q: QueryRequest):
    try:
        return StreamingResponse(agent.stream_bot_response(q.query, q.history))
    except:
        pass
    finally:
        print('LOGGING LOGIC')
