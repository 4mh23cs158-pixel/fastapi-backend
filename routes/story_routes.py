from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Story

from repositories.story_repo import StoryRepo
from schemas.story_schemas import StoryCreate
from services.gemini_service import generate_story

router = APIRouter(
    prefix="/stories",
    tags=["Stories"]
)


@router.post("/")
def create_story(
    story: StoryCreate,
    db: Session = Depends(get_db)
):

    story_text = generate_story(story)

    new_story = Story(

        user_id=1,

        title=story.title,

        description=story.description,

        theme=story.theme,

        genre=story.genre,

        language=story.language,

        age_group=story.age_group,

        story_length=story.story_length,

        art_style=story.art_style,

        moral=story.moral,

        character_name=story.character_name,

        character_type=story.character_type,

        story_content=story_text,

        status="Completed"

    )

    repo = StoryRepo(db)

    saved_story = repo.create_story(new_story)

    return {

        "message": "Story generated successfully",

        "story_id": saved_story.id,

        "title": saved_story.title,

        "story": saved_story.story_content

    }