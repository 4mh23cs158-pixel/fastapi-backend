from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Story, StoryScene

from repositories.story_repo import StoryRepo
from schemas.story_schemas import StoryCreate

from services.gemini_service import generate_story
from services.image_service import ImageService

router = APIRouter(
    prefix="/stories",
    tags=["Stories"]
)


@router.post("/")
def create_story(
    story: StoryCreate,
    db: Session = Depends(get_db)
):

    # Generate Story + Scenes
    story_data = generate_story(story)

    story_text = story_data["story"]

    # Create Story
    new_story = Story(
        user_id=1,
        title=story_data["title"],
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

    generated_scenes = []

    # Generate image for every scene
    for scene in story_data["scenes"]:

        image_path = ImageService.generate_image(
            scene["image_prompt"]
        )

        new_scene = StoryScene(
            story_id=saved_story.id,
            scene_number=scene["scene_number"],
            scene_title=scene["scene_title"],
            scene_text=scene["scene_text"],
            image_prompt=scene["image_prompt"],
            image_path=image_path
        )

        repo.create_scene(new_scene)

        generated_scenes.append({
            "scene_number": scene["scene_number"],
            "scene_title": scene["scene_title"],
            "scene_text": scene["scene_text"],
            "image": image_path
        })

    # Save first image as cover image
    if generated_scenes:
        saved_story.cover_image = generated_scenes[0]["image"]
        db.commit()
        db.refresh(saved_story)

    return {
        "message": "Story generated successfully",
        "story_id": saved_story.id,
        "title": saved_story.title,
        "story": saved_story.story_content,
        "cover_image": saved_story.cover_image,
        "scenes": generated_scenes
    }


@router.get("/{story_id}")
def get_story(
    story_id: int,
    db: Session = Depends(get_db)
):

    repo = StoryRepo(db)

    story = repo.get_story_by_id(story_id)

    if not story:
        return {
            "message": "Story not found"
        }

    scenes = []

    for scene in story.scenes:

        scenes.append({
            "scene_number": scene.scene_number,
            "scene_title": scene.scene_title,
            "scene_text": scene.scene_text,
            "image": scene.image_path
        })

    return {
        "story_id": story.id,
        "title": story.title,
        "story": story.story_content,
        "cover_image": story.cover_image,
        "scenes": scenes
    }


@router.get("/generate-test-image")
def generate_test_image():

    image = ImageService.generate_image(
        """
        Cute baby elephant wearing a blue hat,
        Pixar style,
        children's storybook illustration,
        magical forest,
        vibrant colors,
        3D animation,
        high quality
        """
    )

    return {
        "image": image
    }