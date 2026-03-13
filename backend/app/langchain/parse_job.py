from openai import OpenAI
import json

client = OpenAI()

def parse_job_from_content(title: str, description: str, user_job_skill_names: list[str]):
    user_skill_names = user_job_skill_names

    # Build the prompt
    prompt = f"""
Given the following job title and description{',' if user_skill_names else ''}{" and the user's existing skills" if user_skill_names else ''}, do the following:
1. Write a one-paragraph summary of the job.
2. Return a list of required skills for the job, that someone could go and learn. If a required skill matches or is very similar to one of the user's existing skills, use the exact name from the user's skills list. Otherwise, create a new skill name, for example if "Python" exists in the list, don't return "Python programming", return "Python".

Please make the skill list as concise as possible, only including skills that someone would learn through lessons or a course, also don't combine skills together, they should each be individual skills.
Please keep the number of skills between 1-6, only listing the most important skills.

Job Title: {title}
Job Description: {description}
"""
    if user_skill_names:
        prompt += f"\nUser's existing skills:\n{', '.join(user_skill_names)}\n"

    prompt += """
Respond ONLY in the following JSON format, and NOT as markdown:
{
    "summary": "<job summary here>",
    "skills": ["Skill1", "Skill2", ...]
}
"""
    print("\n\n\n\n")
    print("--------------------------------")
    print(f"workplan prompt: {prompt}")
    print("--------------------------------")
    print("\n\n\n\n")

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    print("\n\n\n\n")
    print("--------------------------------")
    print(f"response: {content}")
    print("--------------------------------")
    print("\n\n\n\n")

    # Try to parse the response as JSON
    try:
        data = json.loads(content)
        summary = data.get("summary", "")
        skills = data.get("skills", [])
    except Exception as e:
        summary = ""
        skills = []
        print(f"Failed to parse LLM response as JSON: {e}\nResponse was: {content}")

    return summary, skills

