
import openai
import streamlit as st
import random

# Safe method to load API key
def set_api_key():
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# 1. Prompt Recognition (Simple vs. Complex)
def is_complex(prompt):
    keywords = ['compare', 'analyze', 'evaluate', 'multi', 'philosophy', 'ethics']
    return any(word in prompt.lower() for word in keywords)

# 2. Epistemic Mode Classifier
def classify_mode(prompt):
    if "what is" in prompt.lower():
        return "factual"
    elif any(x in prompt.lower() for x in ["could", "might", "should"]):
        return "speculative"
    elif "imagine" in prompt.lower():
        return "narrative"
    else:
        return "ambiguous"

# 3. Simulate Contradiction and Entropy Scores
def simulate_scores():
    return {
        "contradiction_score": random.randint(0, 5),
        "entropy_score": random.uniform(0, 1)
    }

# 4. ΔK Control Gate Logic
def should_generate(contradiction_score, entropy_score, mode):
    if contradiction_score > 3 or entropy_score > 0.7 or mode == "ambiguous":
        return False
    return True

# 5. Generate Output Using GPT-4
def generate_output(prompt):
    set_api_key()  # Ensure API key is loaded before making requests
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with epistemic awareness."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# 6. Main SKE Wrapper
def run_ske(prompt):
    st.write(f"**Prompt:** {prompt}")
    
    complex_flag = is_complex(prompt)
    st.write(f"> Prompt Complexity: {'Complex' if complex_flag else 'Simple'}")
    
    mode = classify_mode(prompt)
    st.write(f"> Epistemic Mode: {mode}")
    
    scores = simulate_scores()
    st.write(f"> Contradiction Score: {scores['contradiction_score']} / 5")
    st.write(f"> Entropy Score: {scores['entropy_score']:.2f}")
    
    if should_generate(scores['contradiction_score'], scores['entropy_score'], mode):
        st.success("> ΔK Gate: PASS — Generating Output")
        output = generate_output(prompt)
    else:
        st.warning("> ΔK Gate: FAIL — Responding with Hedge/Defer Mode")
        output = "This question may involve ambiguity or contradiction. Please clarify or rephrase."
    
    st.markdown(f"**Response:** {output}")

# Streamlit UI
st.title("SKE Wrapper Prototype")
user_prompt = st.text_input("Enter your prompt:")

if user_prompt:
    with st.spinner("Evaluating..."):
        run_ske(user_prompt)
