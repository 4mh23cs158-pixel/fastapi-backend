from services.gemini_service import generate_story

class Dummy:

    title="Leo"

    theme="Friendship"

    genre="Adventure"

    character_name="Leo"

    character_type="Lion"

    language="English"

    age_group="5-8"

    story_length="Medium"

    art_style="Pixar"

    moral="Kindness"

story = generate_story(Dummy())

print(story)