import uvicorn
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

from fastapi_demo.api.routers import product_api, user_api

app = FastAPI()

# origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(product_api.router)
app.include_router(user_api.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
