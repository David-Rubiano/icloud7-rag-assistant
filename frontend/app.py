import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Asistente Documental IC7", layout="wide")
st.title("Asistente Documental RAG - I Cloud Seven")

# ... (código anterior igual)

# ==========================================
# SIDEBAR: Subida e Indexación
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # NUEVO: Selector de almacenamiento en la UI
    storage_option = st.radio(
        "Destino de almacenamiento:",
        ["📁 Local (Disco)", "☁️ AWS S3 (Nube)"]
    )
    # Convertimos la selección a un booleano para enviarlo al backend
    use_s3 = "true" if "AWS S3" in storage_option else "false"

    st.divider()

    st.header("1. Panel de Subida de Docs")
    uploaded_files = st.file_uploader(
        "Selecciona archivos (PDF, TXT, MD)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )
    
    if st.button("Subir Documentos"):
        if uploaded_files:
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue(), file.type)}
                
                # Enviamos el parámetro use_s3 en la URL
                resp = requests.post(f"{BACKEND_URL}/upload?use_s3={use_s3}", files=files)
                
                if resp.status_code == 200:
                    st.success(f"Subido exitosamente en {'S3' if use_s3=='true' else 'Local'}: {file.name}")
                else:
                    st.error(f"Error subiendo {file.name}: {resp.text}")
        else:
            st.warning("Por favor, selecciona al menos un archivo primero.")

    st.divider()
    
    st.header("2. Indexación & Chunking")
    if st.button("Ejecutar /proceso_index", type="primary"):
        with st.spinner(f"Leyendo documentos desde {'AWS S3' if use_s3=='true' else 'Local'} y generando embeddings..."):
            
            # Enviamos el parámetro use_s3 en la URL
            resp = requests.post(f"{BACKEND_URL}/proceso_index?use_s3={use_s3}")
            
            if resp.status_code == 200:
                data = resp.json()
                st.success(
                    f"¡Indexación completada!\n\n"
                    f"Documentos leídos de {'S3' if use_s3=='true' else 'Local'}: {data['documents_processed']}\n"
                    f"Fragmentos guardados: {data['chunks_indexed']}"
                )
            else:
                st.error(f"Error en la indexación: {resp.text}")

# ... (El panel principal de Chat queda exactamente igual)

# Panel Principal: Interfaz de Chat / Fuentes
st.header("3. Interfaz de Consulta Documental")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("Ver fragmentos y fuentes recuperadas (ChromaDB)"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.markdown(f"**Fuente #{idx}: `{src['document_name']}`** (Distancia/Score: `{src['similarity_score']}`)")
                    st.caption(src["fragment_preview"])

if prompt := st.chat_input("Escribe tu pregunta sobre los documentos internos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando contexto en ChromaDB y generando respuesta..."):
            resp = requests.post(f"{BACKEND_URL}/Preguntar", json={"question": prompt, "top_k": 3})
            if resp.status_code == 200:
                data = resp.json()
                answer = data["answer"]
                sources = data["sources"]
                st.markdown(answer)
                if sources:
                    with st.expander("Ver fragmentos y fuentes recuperadas (ChromaDB)"):
                        for idx, src in enumerate(sources, 1):
                            st.markdown(f"**Fuente #{idx}: `{src['document_name']}`** (Score: `{src['similarity_score']}`)")
                            st.caption(src["fragment_preview"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            else:
                st.error(f"Error del servidor: {resp.text}")