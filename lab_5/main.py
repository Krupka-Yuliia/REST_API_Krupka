from fastapi import FastAPI
from views import library
import uvicorn

app = FastAPI()
app.include_router(library, prefix="/v1/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
