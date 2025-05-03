import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/chatbot"

st.title("ULTIMATRIX.ai")
st.write("Ask me anything!")

query = st.text_input("Your question:", "")

if st.button("Ask"):
    if query:
        try:
            response = requests.post(FASTAPI_URL, headers={"Content-Type": "application/json"}, json={"query": query})
            if response.status_code == 200:
                answer = response.json().get("answer", "No response.")
            else:
                answer = f"❌ API Error: {response.status_code}"
        except Exception as e:
            answer = f"❌ Request failed: {e}"

        # Display the chatbot response
        st.markdown(f"Answer:\n{answer}")  # Better formatting
    else:
        st.warning("Please enter a question!")