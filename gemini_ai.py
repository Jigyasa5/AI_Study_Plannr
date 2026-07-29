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
Hours Per Day: {hours}
Difficulty: {difficulty}

Generate:
1. Daily timetable
2. Weekly goals
3. Revision strategy
4. Important topics
5. Motivation tips

Format the response neatly using headings and bullet points.
"""

    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt,
    )

    return response.text