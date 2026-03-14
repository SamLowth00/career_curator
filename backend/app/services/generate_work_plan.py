from openai import OpenAI

client = OpenAI()

LEVEL_LABELS = {1: "Beginner", 2: "Intermediate", 3: "Expert"}

SYSTEM_PROMPT = """You are an expert career coach and learning strategist. Your task is to create a personalised, holistic career development plan based on the skills required across a set of job listings and what the user already knows.

Rules:
1. Treat all required skills as part of one interconnected learning journey — do NOT write a separate breakdown per skill.
2. Prioritise skills by their mention count (higher = more important to employers). Weave frequently-mentioned skills earlier and more prominently into the plan.
3. Personalise using the user's existing skills:
   - Skip or briefly acknowledge skills they already have at Intermediate or Expert level — focus on gaps and advanced progression instead.
   - For skills at Beginner level, fast-track past the basics.
   - For skills they have no experience with, include full foundational steps.
4. Structure the plan as a phased learning roadmap (e.g. Phase 1: Foundations, Phase 2: Core Skills, Phase 3: Advanced & Integration). Each phase should have:
   - A clear goal and rationale
   - Specific, actionable steps with named real resources (actual course names, book titles, official docs — never generic placeholders)
   - Realistic time estimates per phase
5. Close with 1-2 specific capstone project ideas that tie multiple skills together and would stand out on a portfolio.

FORMAT: Use clean markdown with ## headings for each phase, numbered steps, and **bold resource names**. Be direct and specific — no vague advice."""


def generate_work_plan(skills_with_counts: list, user_skills: list = None):
    if skills_with_counts:
        skills_text = ", ".join(f"{name} - {count}" for name, count in skills_with_counts)
    else:
        skills_text = "No skills provided"

    user_message = f"Required skills for target roles (number of job mentions): {skills_text}"

    if user_skills:
        lines = []
        for s in user_skills:
            level_label = LEVEL_LABELS.get(s.get("level"), "Unknown")
            desc = f" — {s['description']}" if s.get("description") else ""
            lines.append(f"- {s['name']} ({level_label}){desc}")
        user_message += "\n\nUser's existing skills:\n" + "\n".join(lines)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
