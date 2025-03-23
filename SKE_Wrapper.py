
# 4. Recursive Revision Layer (Strict Mode)
def revise_answer(prompt, answer, audit_summary=None):
    """
    Revises the answer based on contradiction pressure and hallucination detection.
    If hallucination is high (Ψ >= 3), avoids speculation unless user requests it.
    """
    system_prompt = (
        "You are an epistemically responsible assistant tasked with correcting hallucinations in AI-generated text. "
        "If the provided answer is based on a fictional or non-existent concept (e.g., a fake book, person, or event), "
        "you must clearly state that the subject does not exist. Do not speculate, elaborate, or interpret unless the user explicitly requests that. "
        "Your revision should end with an offer like: 'If you’d like, I can speculate based on known themes or patterns—just let me know.'"
    )

    revision_prompt = f"""The user prompt was:
{prompt}

The AI's original answer was:
{answer}

Epistemic audit summary:
{audit_summary}

Revise the answer to eliminate hallucination and speculation unless explicitly requested. Prioritize truthfulness and clarity."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": revision_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error in strict revise_answer] {e}"
