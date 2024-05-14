from pydantic import BaseModel, ConfigDict, Field

# constants for examples
TITLE = "My vacancy title"
DESCRIPTION = "My vacancy description"


class Example(BaseModel):
    id: int
    title: str = Field(max_length=256, examples=[TITLE])
    description: str = Field(max_length=2000, examples=[DESCRIPTION])
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
