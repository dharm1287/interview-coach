import os
import json
import openai
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', settings.OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

QUESTION_TEMPLATE = (
    "You are an experienced interviewer for the role: {role}. The candidate level: {level}."
    " Produce one concise interview question (suitable for a live interview). Return only the question text."
)

FEEDBACK_TEMPLATE = (
    "You are an interviewer and coach. Given the question:\n{question}\nand the candidate answer:\n{answer}\n"
    "Evaluate the answer on these dimensions (0-5): relevance, clarity, correctness, specificity, communication."
    " Return a JSON object with keys: scores (mapping), overall (number), strengths (list), weaknesses (list), improvement_tips (list), model_answer (string)."
)


def generate_question(role: str, level: str) -> str:
    prompt = QUESTION_TEMPLATE.format(role=role, level=level)
    resp = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user','content':prompt}],
        temperature=0.7,
        max_tokens=150,
    )
    text = resp.choices[0].message.content.strip()
    # try to sanitize if LLM returns JSON etc.
    return text


def evaluate_answer(question: str, answer: str, role: str) -> dict:
    prompt = FEEDBACK_TEMPLATE.format(question=question, answer=answer)
    resp = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user','content':prompt}],
        temperature=0.0,
        max_tokens=450,
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except Exception:
        # fallback: return raw text in a dict
        return {'raw_feedback': raw}
