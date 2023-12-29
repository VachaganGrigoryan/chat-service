import asyncio

from uvicorn import Server, Config

from app import app


async def main():
    config = Config(
        app=app,
        port=5000,
        loop='asyncio',
        log_level='debug',
        reload=True,
        reload_dirs=['./app'],
        reload_includes=['*.py'],
        workers=2,
    )
    server = Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
