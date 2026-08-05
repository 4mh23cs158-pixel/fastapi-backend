def build_story_prompt(data):

    return f"""
You are an expert children's story writer.

Generate an original children's story.

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

----------------------------------------

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT use ```json.

Format:

{{
"title":"",

"story":"",

"scenes":[

{{
"scene_number":1,

"scene_title":"",

"scene_text":"",

"image_prompt":""
}}

]

}}

Rules:

1. Story should have beginning, middle and ending.

2. Story should contain dialogues.

3. Story should be emotional.

4. Divide story into 4 scenes.

5. scene_text should summarize only that scene.

6. image_prompt must describe ONLY that scene.

7. image_prompt must include:

• character appearance

• clothes

• facial expressions

• environment

• lighting

• colors

• Pixar style

• children's storybook illustration

Return ONLY JSON.
"""