
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. Epistemic Mode Detection
def epistemic_mode(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Classify the following prompt as factual, speculative, narrative, or ambiguous."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error in epistemic_mode] {e}"

# 2. First-pass answer
def generate_first_pass(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful, epistemically aware assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error in generate_first_pass] {e}"

# 3. Audit for contradiction pressure (Ψ)
def audit_response(prompt, answer):
    try:
        audit_prompt = f"""Evaluate the following AI response for epistemic reliability.

Prompt: {prompt}

Answer: {answer}

Does the answer contain contradiction, hallucination, or uncertainty? Rate the contradiction pressure (Ψ) from 0 (none) to 5 (severe), and explain briefly.
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an epistemic auditor."},
                {"role": "user", "content": audit_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error in audit_response] {e}"

# 4. Strict hallucination-aware revision logic
def revise_answer(prompt, answer, audit_summary=None):
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

# Streamlit Interface
st.title("SKE Phase II – Strict Hallucination Handling")

user_prompt = st.text_input("Enter your prompt:")

if user_prompt:
    with st.spinner("Classifying epistemic mode..."):
        mode = epistemic_mode(user_prompt)
        st.write(f"**Epistemic Mode:** {mode}")

    with st.spinner("Generating first-pass answer..."):
        answer = generate_first_pass(user_prompt)
        st.write("**First-Pass Answer:**")
        st.markdown(answer)

    with st.spinner("Auditing for contradiction pressure..."):
        audit = audit_response(user_prompt, answer)
        st.write("**ΔK Audit Result:**")
        st.markdown(audit)

    with st.spinner("Revising answer with strict hallucination policy..."):
        revised = revise_answer(user_prompt, answer, audit_summary=audit)
        st.write("**Revised Answer:**")
        st.markdown(revised)
