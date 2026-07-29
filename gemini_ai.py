import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_plan(subject, exam_date, hours, difficulty):

    prompt = f"""
    Create a personalized study plan.

    Subject: {subject}
    Exam Date: {exam_date}
    Study Hours Per Day: {hours}
    Difficulty: {difficulty}

    Return ONLY valid HTML.

    Requirements:
    - Use <h2> for section headings.
    - Use <h3> for subsection headings.
    - Use <p> for paragraphs.
    - Use <ul><li> for bullet points.
    - Use <table>, <tr>, <th>, and <td> for the daily timetable.
    - Use <strong> to highlight important points.
    - Do NOT use Markdown symbols such as #, ##, **, |, or ---.

    Include:
    1. Daily Timetable
    2. Weekly Goals
    3. Revision Strategy
    4. Important Topics
    5. Practice Plan
    6. Motivation Tips

"""

    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt,
    )

    return response.text