from openai import OpenAI
import json

client = OpenAI()

SYSTEM_PROMPT = """You are an expert job analyst. Your task is to extract a concise summary and a list of key learnable skills from a job listing.

Rules for skills:
1. Only include concrete, nameable skills that can be learned through study, training, or practice — specific tools, methodologies, techniques, certifications, or domain knowledge.
2. Do NOT include soft skills, personality traits, or vague competencies (e.g. "communication", "problem solving", "team player", "analytical thinking").
3. Name each skill as concisely as possible — a short noun or noun phrase with no filler words like "techniques" or "skills".
4. If a required skill matches or is very similar to one of the user's existing skills, use the exact name from that list.
5. Otherwise, create a new concise skill name.
6. Do not combine multiple skills into one entry — each skill must be a single, distinct concept.
7. Include between 3 and 8 skills, prioritising the most important ones.

Example of bad skill output: ["Communication", "Technical knowledge", "Problem solving", "Working in a team"]
Example of good skill output: a short list of specific, learnable, nameable skills relevant to the role

Respond ONLY in the following JSON format, not as markdown:
{
    "summary": "<one-paragraph job summary>",
    "skills": ["Skill1", "Skill2", ...]
}"""


def parse_job_from_content(title: str, description: str, user_job_skill_names: list[str]):
    user_skill_names = user_job_skill_names

    user_message = f"Job Title: {title}\n\nJob Description:\n{description}"

    if user_skill_names:
        user_message += f"\n\nUser's existing skills (match these where possible):\n{', '.join(user_skill_names)}"

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
    )
    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        summary = data.get("summary", "")
        skills = data.get("skills", [])
    except Exception as e:
        summary = ""
        skills = []
        print(f"Failed to parse LLM response as JSON: {e}\nResponse was: {content}")

    return summary, skills
