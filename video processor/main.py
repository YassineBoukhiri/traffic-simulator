from fastapi import FastAPI
import uvicorn
from router import router


app = FastAPI(
    title= "Video Processor API",
    version="1.0.0",
    docs_url="/",
    redoc_url="/docs",
    description="This is a REST API for the Video processor service.",
)

# include route
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port=8001)