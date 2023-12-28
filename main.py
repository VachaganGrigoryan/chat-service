
import uvicorn
from uvicorn import Server

from app.api import app


if __name__ == "__main__":
    server = Server(config=uvicorn.Config(app, workers=1, loop="asyncio", reload=True))

    server.run()
