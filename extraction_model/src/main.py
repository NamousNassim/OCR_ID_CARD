import sys
import os
from fastapi import FastAPI


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import router

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)