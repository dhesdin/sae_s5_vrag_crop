

from fastapi import APIRouter


class ResponsesRouter(APIRouter):

    def __init__(self) -> None:
        super().__init__(prefix="/responses", tags=["responses"])
        self._register_endpoints()

    def _register_endpoints(self):
        self.get("/", response_model=dict)(self.root)
        self.get("/all", response_model=dict)(self.get_all_responses)

    async def root(self) -> dict:
        return {"message": "Responses route"}

    async def get_all_responses(self) -> dict:
        return {
            "message": "Getting all responses",
            "content": []
        }