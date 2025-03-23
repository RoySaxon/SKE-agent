
import streamlit as st
import openai

# Load API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 1. Epistemic Intent Classifier
def epistemic_mode(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You classify the epistemic intent of a prompt as one of: factual, speculative, narrative, or ambiguous."},
            {"role": "user", "content": f"Prompt: {prompt}\nClassify the intent."}
        ]
    )
    return response.choices[0].message["content"].strip()

# 2. First Pass Answer Generator
def generate_first_pass(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, epistemically-aware assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"].strip()

# 3. ΔK Audit Layer
def audit_response(prompt, answer):
    audit_prompt = f"""Evaluate the following response for epistemic reliability.

Prompt: {prompt}

Answer: {answer}

Does the answer contain contradiction, hallucination, or uncertainty? Rate the contradiction pressure (Ψ) from 0 (none) to 5 (severe), and explain briefly.
""" 
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an epistemic auditor."},
            {"role": "user", "content": audit_prompt}
        ]
    )
    return response.choices[0].message["content"].strip()

# 4. Recursive Revision Layer
def revise_answer(prompt, answer):
    revise_prompt = f"""Your previous answer may have contained contradictions or uncertainty.

Prompt: {prompt}

Original Answer: {answer}

Revise the answer to be more epistemically robust. Hedge if needed, or reframe with greater precision.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that improves epistemic reliability."},
            {"role": "user", "content": revise_prompt}
        ]
    )
    return response.choices[0].message["content"].strip()

# Streamlit UI
st.title("SKE Phase II: Recursive Epistemic Agent")

user_prompt = st.text_input("Enter your prompt:")
if user_prompt:
    with st.spinner("Classifying epistemic mode..."):
        mode = epistemic_mode(user_prompt)
        st.write(f"**Epistemic Mode:** {mode}")

    with st.spinner("Generating first-pass answer..."):
        answer = generate_first_pass(user_prompt)
        st.write(f"**First-Pass Answer:** {answer}")

    with st.spinner("Auditing for contradiction pressure..."):
        audit = audit_response(user_prompt, answer)
        st.write("**ΔK Audit Result:**")
        st.markdown(audit)

    if "Ψ" in audit or "contradiction" in audit.lower():
        with st.spinner("Revising based on epistemic audit..."):
            revised = revise_answer(user_prompt, answer)
            st.write("**Revised Answer:**")
            st.markdown(revised)
