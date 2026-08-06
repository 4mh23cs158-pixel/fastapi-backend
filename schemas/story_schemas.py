from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    theme: str
    genre: str
    language: Optional[str] = None
    age_group: Optional[str] = None
    story_length: Optional[str] = None
    art_style: Optional[str] = None
    moral: Optional[str] = None
    cover_image: Optional[str] = None
    status: Optional[str] = "Draft"
    visibility: Optional[str] = "Private"
    last_opened: Optional[datetime] = None

class StoryCreate(BaseModel):
    user_id: int
    title: str

    description: Optional[str] = None

    theme: str

    genre: Optional[str] = None

    language: str

    age_group: str

    story_length: str

    art_style: str

    moral: str

    character_name: str

    character_type: str


class StoryResponse(BaseModel):

    id: int

    user_id: int

    title: str

    description: Optional[str]

    theme: str

    genre: Optional[str]

    language: str

    age_group: str

    story_length: str

    art_style: str

    moral: Optional[str]

    status: str

    visibility: str

    created_at: datetime

    class Config:
        from_attributes = True