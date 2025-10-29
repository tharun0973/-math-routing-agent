import re

def validate_input(question: str) -> bool:
    # Basic profanity and off-topic filter
    banned = ["kill", "sex", "politics", "violence"]
    if any(word in question.lower() for word in banned):
        return False
    return bool(re.search(r'\d|\+|\-|\*|\/|=|x', question))

def sanitize_output(answer: str) -> str:
    # Remove hallucinated phrases
    return answer.replace("I'm not sure", "").strip()

