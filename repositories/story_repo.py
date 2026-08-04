from sqlalchemy.orm import Session
from models import Story


class StoryRepo:

    def __init__(self, db: Session):
        self.db = db

    def create_story(self, story: Story):
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story

    def get_story_by_id(self, story_id: int):
        return self.db.query(Story).filter(
            Story.id == story_id
        ).first()

    def get_user_stories(self, user_id: int):
        return self.db.query(Story).filter(
            Story.user_id == user_id
        ).all()

    def delete_story(self, story_id: int):
        story = self.get_story_by_id(story_id)

        if story:
            self.db.delete(story)
            self.db.commit()

        return story