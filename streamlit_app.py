import streamlit as st
import requests

# ✅ Update this URL to match your FastAPI deployment
FASTAPI_URL = "http://127.0.0.1:8000/chatbot"

st.title("ULTIMATRIX.ai 🤖")
st.write("Ask me anything!")

# ✅ Improved user input area
query = st.text_input("💬 Your question:")

if st.button("Ask"):
    if query.strip():  # ✅ Prevents empty input
        try:
            # ✅ Updated API request with correct endpoint
            response = requests.post(
                FASTAPI_URL, headers={"Content-Type": "application/json"}, json={"query": query}
            )

            # ✅ Improved response handling
            if response.status_code == 200:
                answer = response.json().get("answer", "No response.")
            else:
                answer = f"❌ API Error {response.status_code}: {response.json().get('detail', 'Unknown error')}"

        except requests.exceptions.RequestException as e:
            answer = f"❌ Request failed: {str(e)}"

        # ✅ Better display formatting
        st.markdown(f"### 🤖 Answer:\n{answer}")

    else:
        st.warning("⚠️ Please enter a valid question.")
