from pydantic import BaseModel

class SuggestRequest(BaseModel):
    host_element: str
    adjacent_element: str
    exposure: str