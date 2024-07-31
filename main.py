from fastapi import FastAPI
from app import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.project.router)
app.include_router(routers.sub_task.router)
app.include_router(routers.user.router)
app.include_router(routers.tasks.router)
app.include_router(routers.tags.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}