from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Image Host API",
    description="Development",
    version="1.0",
    default_response_class=ORJSONResponse
)


@app.get("/")
async def root():
    """Health check."""
    # return {"status_code": 200, "detail": "Healthy!"}
    return ORJSONResponse(
        content={"detail": "Healthy!"}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    expose_headers=["Content-Range", "Range"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )
    