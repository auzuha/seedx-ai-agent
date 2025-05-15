from fastapi import FastAPI

from fastapi.responses import StreamingResponse

from agent.graph import get_agent


from models.models import QueryRequest

app = FastAPI()
agent = get_agent()


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
