import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Shopping Assistant", page_icon="🛒", layout="centered")

st.title("🛒 AI Shopping Assistant")
st.caption("Ask me about products, comparisons, or recommendations")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What are you looking for?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = httpx.post(
                    f"{API_URL}/api/v1/chat",
                    json={"message": prompt},
                    timeout=120.0,
                )
                data = r.json()
                response = data.get("response", "Sorry, I couldn't process that.")
            except Exception as e:
                response = f"Error: {e}"

        st.markdown(response)

        products = data.get("products", []) if "data" in dir() else []
        if products:
            st.subheader("Recommended Products")
            for p in products[:5]:
                cols = st.columns([3, 1])
                cols[0].write(f"**{p.get('title', '')}**")
                cols[1].write(f"₹{p.get('price', 0):,.0f}")

    st.session_state.messages.append({"role": "assistant", "content": response})
