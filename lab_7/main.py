from fastapi import FastAPI
from views import main
from auth_routes import router
from models import Base
from database import engine
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(main, prefix="/v1/api")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5050)