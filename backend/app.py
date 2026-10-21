
    
from fastapi import FastAPI

from routers.responsesRouter import ResponsesRouter


class App(FastAPI):

    def __init__(self) -> None:
        super().__init__(title="API")
        self._register_endpoints()
        self._register_routers()

    def _register_routers(self) -> None:
        self.include_router(ResponsesRouter())

    def _register_endpoints(self) -> None:
        self.get("/", response_model=dict)(self.root)
        self.get("/health", response_model=dict)(self.health)

    async def root(self) -> dict:
        return {"message": "Hello, World!"}

    async def health(self) -> dict:
        return {"status": "healthy"}