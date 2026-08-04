def build_story_prompt(data):

    return f"""
Write a beautiful children's story.

Title:
{data.title}

Theme:
{data.theme}

Genre:
{data.genre}

Main Character:
{data.character_name}

Character Type:
{data.character_type}

Language:
{data.language}

Age Group:
{data.age_group}

Story Length:
{data.story_length}

Art Style:
{data.art_style}

Moral:
{data.moral}

Requirements:

1. Give the story a proper title.
2. Include dialogues.
3. Make the story interesting.
4. Add emotions.
5. Include a beginning, middle and ending.
6. End with the moral.
7. Return ONLY the story text.
"""