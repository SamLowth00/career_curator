from langchain_community.llms import OpenAI
import json

def parse_job_with_langchain(title: str, description: str, user_skill_names: list[str]):
    # Build the prompt
    prompt = f"""
Given the following job title and description{',' if user_skill_names else ''}{' and the user\'s existing skills' if user_skill_names else ''}, do the following:
1. Write a one-paragraph summary of the job.
2. Return a list of required skills for the job, that someone could go and learn. If a required skill matches or is very similar to one of the user's existing skills, use the exact name from the user's skills list. Otherwise, create a new skill name, for example if "Python" exists in the list, don't return "Python programming", return "Python".

Please make the skill list as concise as possible, only including skills that someone would learn through lessons or a course, also don't combine skills together, they should each be individual skills.

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
    print(f"prompt: {prompt}")
    llm = OpenAI(temperature=0.2)
    response = llm(prompt)
    print(f"resp {response}")
    # Try to parse the response as JSON
    try:
        data = json.loads(response)
        summary = data.get("summary", "")
        skills = data.get("skills", [])
    except Exception as e:
        # Fallback: return raw response if parsing fails
        summary = ""
        skills = []
        print(f"Failed to parse LLM response as JSON: {e}\nResponse was: {response}")

    return summary, skills

