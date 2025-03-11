from fastapi import FastAPI
from views import main

app = FastAPI()

app.include_router(main, prefix="/v1/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5050)
