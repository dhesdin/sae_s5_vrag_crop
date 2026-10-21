
    
from fastapi import FastAPI


class App(FastAPI):

    def __init__(self) -> None:
        super().__init__(title="API")
        self._register_routes()

    def _register_routes(self) -> None:
        self.get("/", response_model=dict)(self.root)
        self.get("/health", response_model=dict)(self.health)

    async def root(self) -> dict:
        return {"message": "Hello, World!"}

    async def health(self) -> dict:
        return {"status": "healthy"}