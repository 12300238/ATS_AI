import streamlit as st


def show_assistant():

    st.title("🤖 Assistant IA")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input(
        "Posez votre question..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        response = """
        Pour améliorer votre CV :
        
        • Ajoutez plus de mots-clés ATS
        • Détaillez vos projets
        • Ajoutez des résultats chiffrés
        """

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):
            st.write(response)