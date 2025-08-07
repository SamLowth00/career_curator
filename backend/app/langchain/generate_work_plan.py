from typing import List
from app.models import Skill
import json
# from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


def generate_work_plan(list_of_skills: List[str]):
    prompt = f"""Create a concise but comprehensive study plan for these skills: {', '.join(list_of_skills) if list_of_skills else 'No skills provided'}

For EACH skill, provide:
1. **Overview**: What it is and why it's valuable (2-3 sentences)
2. **Learning Steps**: 3-5 specific, actionable steps to master this skill
3. **Resources**: 2-3 specific courses/books/projects with names
4. **Time**: Realistic time estimate for each step
5. **Prerequisites**: Any foundational knowledge needed

FORMAT: Use clean markdown with clear headings. Be concise but specific. Focus on actionable steps rather than lengthy explanations.

If multiple skills, suggest learning order and include 1-2 cross-skill projects."""
    
    print("\n\n\n\n")
    print("--------------------------------")
    print(f"workplan prompt: {prompt}")
    print("--------------------------------")
    print("\n\n\n\n")

    llm = ChatOpenAI(temperature=0.2, model="gpt-4")
    response = llm([HumanMessage(content=prompt)])

    return response.content

        