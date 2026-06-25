import streamlit as st

from rag_pipeline import build_rag_pipeline

# PAGE CONFIG

st.set_page_config(
    page_title="BioFlow AI",
    page_icon="🧬",
    layout="wide"
)

# HEADER

st.title("🧬 BioFlow AI")
st.subheader("Bioinformatics Workflow Copilot")
st.info(
    """
    BioFlow AI helps students and junior researchers
    choose bioinformatics tools and workflows based on
    curated bioinformatics knowledge sources.
    """
)

st.markdown(
    """
    Ask questions about:

    - Bioinformatics workflows
    - Tool selection
    - RNA-Seq analysis
    - Variant calling
    - Quality control
    - Best practices
    """
)

# LOAD RAG PIPELINE

@st.cache_resource
def load_chain():
    return build_rag_pipeline()

chain, num_chunks = load_chain()

# SIDEBAR

with st.sidebar:

    st.header("Project Information")

    st.metric(
        "Knowledge Base Size",
        f"{num_chunks} Chunks"
    )

    st.metric(
        "Top-K Retrieval",
        "4"
    )

    st.markdown("---")

    st.markdown("""
                
    ### Architecture

    Knowledge Base

    ↓

    Chunking

    ↓

    Embedding

    ↓

    FAISS

    ↓

    Retrieval

    ↓

    Groq LLM
    """
    )

    st.markdown("---")

    st.markdown("### Example Questions")

    st.markdown(
        """
        - What is FastQC?

        - When should I use STAR instead of BWA?

        - Recommend a workflow for RNA-Seq differential expression analysis.

        - What are common beginner mistakes in bioinformatics?

        - Which tool should I use for sequence similarity searching?
        """
    )

# QUESTION INPUT

question = st.text_area(
    "Enter your question",
    height=120
)

# RUN QUERY

if st.button("Generate Answer"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching knowledge base..."):

            try:

                response = chain.invoke(
                    {"query": question}
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

                st.stop()

        answer = response["result"]

        st.markdown("## Answer")

        st.write(answer)

        with st.expander("Retrieved Sources"):

            for i, doc in enumerate(
                response["source_documents"],
                start=1
            ):

                st.markdown(f"### Chunk {i}")

                st.write(doc.page_content[:1000])

st.markdown("---")

st.caption(
    "BioFlow AI | Final Project LLM & RAG | Built with Streamlit, LangChain, FAISS, Groq"
)