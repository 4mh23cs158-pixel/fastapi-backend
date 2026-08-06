from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Story, StoryScene
from models import User
from repositories.user_repo import UserRepo


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
    # Check whether the user exists
    user_repo = UserRepo(db)

    user = user_repo.get_user_by_id(story.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Generate Story + Scenes
    story_data = generate_story(story)

    story_text = story_data["story"]


    new_story = Story(
        user_id=story.user_id,
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


@router.get("/user/{user_id}")
def get_user_stories(
    user_id: int,
    db: Session = Depends(get_db)
):

    user_repo = UserRepo(db)

    user = user_repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    repo = StoryRepo(db)

    stories = repo.get_user_stories(user_id)

    result = []
    for s in stories:
        result.append({
            "story_id": s.id,
            "title": s.title,
            "description": s.description,
            "theme": s.theme,
            "genre": s.genre,
            "language": s.language,
            "age_group": s.age_group,
            "art_style": s.art_style,
            "moral": s.moral,
            "character_name": s.character_name,
            "character_type": s.character_type,
            "cover_image": s.cover_image,
            "created_at": str(s.created_at) if s.created_at else None,
            "scene_count": len(s.scenes) if s.scenes else 0
        })

    return result


@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    repo = StoryRepo(db)
    story = repo.get_story_by_id(story_id)

    if not story:
        raise HTTPException(
            status_code=404,
            detail="Story not found"
        )

    repo.delete_story(story_id)
    
    return {"message": "Story deleted successfully"}

