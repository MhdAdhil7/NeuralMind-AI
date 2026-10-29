
import hashlib
import html
import tempfile
from pathlib import Path

import streamlit as st

from src.pdf_reader import extract_text_from_pdf, extract_pages_from_pdf
from src.text_chunker import chunk_pages
from src.vector_store import store_chunks, search_stored_chunks
from src.answer_generator import generate_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NeuralMind | Private Research Library",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# OLD MONEY DARK THEME
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');

    :root {
        --bg: #09110F;
        --panel: #101B18;
        --panel-soft: #14221D;
        --green: #294638;
        --green-light: #3D604B;
        --gold: #C5A56A;
        --gold-light: #E2C895;
        --ivory: #F0E9DA;
        --muted: #A7AA9E;
        --border: #30443A;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 72% 0%, #18271F 0%, transparent 42%),
            var(--bg);
        color: var(--ivory);
    }

    [data-testid="stHeader"] {
        background: rgba(9, 17, 15, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #0D1713;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: var(--ivory) !important;
        font-weight: 500 !important;
        letter-spacing: -0.4px;
    }

    p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    .brand {
        color: var(--ivory);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.65rem;
        letter-spacing: 3px;
        line-height: 1.3;
    }

    .brand-subtitle {
        color: var(--gold);
        font-size: 0.61rem;
        letter-spacing: 2px;
        margin-top: 5px;
        text-transform: uppercase;
    }

    .eyebrow {
        color: var(--gold);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 2.4px;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2.5rem, 4.5vw, 4.2rem);
        font-weight: 500;
        line-height: 1.12;
        letter-spacing: -1.5px;
        color: var(--ivory);
        margin: 12px 0 18px;
    }

    .hero-description {
        font-size: 1.03rem;
        line-height: 1.85;
        max-width: 670px;
        color: #B7B8AD;
    }

    .gold-line {
        height: 1px;
        background: linear-gradient(90deg, var(--gold), transparent);
        margin: 24px 0;
        opacity: 0.7;
    }

    .lux-card {
        background: linear-gradient(145deg, #14221D, #0D1714);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 22px;
        margin: 8px 0 16px;
    }

    .document-title {
        color: var(--ivory);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.15rem;
    }

    .small-label {
        color: var(--gold);
        font-size: 0.68rem;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 11px;
        border: 1px solid #42634D;
        border-radius: 30px;
        background: #1B3025;
        color: #B8D5BE;
        font-size: 0.75rem;
    }

    .feature-title {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--ivory);
        font-size: 1.12rem;
        margin-bottom: 7px;
    }

    .feature-description {
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.65;
    }

    .quote {
        color: var(--gold-light);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.2rem;
        font-style: italic;
        line-height: 1.7;
    }

    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 37px;
        height: 37px;
        border: 1px solid var(--gold);
        border-radius: 50%;
        color: var(--gold-light);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.1rem;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #0C1713 !important;
        color: var(--ivory) !important;
        border: 1px solid #58624D !important;
        border-radius: 10px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold) !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #858D82 !important;
    }

    /* Antique-gold submit button with readable dark text. */
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(110deg, #D9BD86, #B89559) !important;
        color: #172019 !important;
        -webkit-text-fill-color: #172019 !important;
        border: 1px solid #E0C895 !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        min-height: 45px;
        transition: all 0.2s ease;
    }

    .stButton > button *,
    [data-testid="stFormSubmitButton"] > button * {
        color: #172019 !important;
        -webkit-text-fill-color: #172019 !important;
        opacity: 1 !important;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: #E6D0A5 !important;
        border-color: #E6D0A5 !important;
        transform: translateY(-1px);
    }

    [data-testid="stFileUploader"] {
        background: #111D18;
        border: 1px dashed #6A7057;
        border-radius: 12px;
        padding: 8px;
    }

    [data-testid="stFileUploader"] section {
        background: transparent;
    }

    [data-testid="stExpander"] {
        background: #101B17;
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        color: var(--ivory);
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: var(--border) !important;
    }

    .footer {
        color: #858D82;
        font-size: 0.65rem;
        letter-spacing: 2px;
        text-align: center;
        margin-top: 45px;
        padding: 20px 0 10px;
    }

    .source-reference {
        color: var(--gold);
        font-size: 0.68rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .lux-card {
            padding: 16px;
        }

        .brand {
            font-size: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="font-size:2rem; margin-bottom:8px;">📖</div>
        <div class="brand">NEURALMIND</div>
        <div class="brand-subtitle">The Private Research Library</div>
        <div class="gold-line"></div>
        """,
        unsafe_allow_html=True,
    )
    

    st.markdown("##### YOUR WORKSPACE")

    st.markdown(
        """
        <div class="feature-description" style="margin-bottom: 16px;">
            Your private space for exploring PDF documents
            and verifying answers against their contents.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="small-label">RESEARCH WORKFLOW</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin: 14px 0;">
            <div class="document-title">01 &nbsp; Upload</div>
            <div class="feature-description">
                Add a PDF document to begin.
            </div>
        </div>
        <div style="margin: 14px 0;">
            <div class="document-title">02 &nbsp; Explore</div>
            <div class="feature-description">
                Ask questions about its contents.
            </div>
        </div>
        <div style="margin: 14px 0;">
            <div class="document-title">03 &nbsp; Verify</div>
            <div class="feature-description">
                Review answers and supporting passages.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="small-label">Current document</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        help="Upload a text-based PDF to begin your research.",
    )

    if uploaded_file is None:
        st.caption("No document selected.")
    else:
        safe_filename = html.escape(uploaded_file.name)

        st.markdown(
            f"""
            <div class="lux-card">
                <div class="document-title">▤ &nbsp; Document loaded</div>
                <p style="overflow-wrap:anywhere; margin-bottom:5px;">
                    {safe_filename}
                </p>
                <span class="status-pill">● Selected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="quote">
            “The art of reading is to discover what deserves to be understood.”
        </div>
        <br>
        <div class="small-label">Private · Thoughtful · Evidence-led</div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# MAIN HERO
# --------------------------------------------------

top_left, top_right = st.columns([5, 1])

with top_right:
    st.markdown(
        """
        <div style="text-align:right; padding-top:8px;">
            <span class="status-pill">● Local AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="eyebrow">Intelligence, with discernment</div>
    <div class="hero-title">Knowledge,<br>thoughtfully explored.</div>
    <div class="hero-description">
        A quieter way to understand complex documents. Ask precise
        questions, examine the evidence, and discover what your
        sources actually say.
    </div>
    <div class="gold-line"></div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if uploaded_file is None:
    st.markdown(
        """
        <div class="lux-card">
            <div class="document-title">Begin your research</div>
            <p>
                Your private research library is ready.
                Upload a PDF using the panel on the left to begin.
            </p>
            <div class="small-label">
                Your documents stay in your workflow
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feature_a, feature_b = st.columns(2)

    with feature_a:
        st.markdown(
            """
            <div class="lux-card">
                <div class="feature-title">
                    ♧ &nbsp; Evidence-backed answers
                </div>
                <div class="feature-description">
                    Answers are checked against passages retrieved
                    from your document.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with feature_b:
        st.markdown(
            """
            <div class="lux-card">
                <div class="feature-title">▤ &nbsp; Source references</div>
                <div class="feature-description">
                    Explore the passages and PDF pages behind
                    your answers.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            NEURALMIND AI &nbsp; · &nbsp; PRIVATE &nbsp; · &nbsp;
            LOCAL &nbsp; · &nbsp; YOUR DOCUMENTS, YOUR CONTROL
            <div style="
                margin-top: 12px;
                color: #C5A56A;
                font-family: 'Playfair Display', Georgia, serif;
                font-size: 11px;
                letter-spacing: 1.5px;
                text-transform: lowercase;
            ">
                by mhd adhil
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

document_name = uploaded_file.name
file_bytes = uploaded_file.getvalue()

file_hash = hashlib.sha256(file_bytes).hexdigest()[:16]
document_id = f"{document_name}_{file_hash}"

temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    text = extract_text_from_pdf(temp_path)

    if not text.strip():
        st.warning(
            "No readable text was found. This PDF may contain "
            "scanned images instead of selectable text."
        )
        st.stop()

    pages = extract_pages_from_pdf(temp_path)

    chunks = chunk_pages(
        pages,
        chunk_size=100,
        overlap=20,
    )

    if not chunks:
        st.warning("No text chunks could be created from this document.")
        st.stop()

    stored_document_id = st.session_state.get("stored_document_id")

    if stored_document_id != document_id:
        with st.spinner("Preparing your document for research..."):
            store_chunks(
                chunks,
                document_name=document_id,
            )

        st.session_state["stored_document_id"] = document_id
        st.session_state["document_id"] = document_id

    safe_document_name = html.escape(document_name)

    st.markdown(
        f"""
        <div class="lux-card">
            <div class="small-label">Current research document</div>
            <div class="document-title" style="margin-top:8px;">
                ▤ &nbsp; {safe_document_name}
            </div>
            <p style="margin-top:7px;">
                PDF document · {len(chunks)} text passages prepared
            </p>
            <span class="status-pill">● Ready for examination</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View extracted document text"):
        st.text_area(
            "Extracted PDF text",
            text,
            height=220,
            disabled=True,
        )

except Exception as error:
    st.error(f"Could not process the PDF: {error}")
    st.stop()

finally:
    if temp_path is not None:
        Path(temp_path).unlink(missing_ok=True)


# --------------------------------------------------
# QUESTION FORM
# --------------------------------------------------

st.markdown(
    """
    <div class="eyebrow">Your inquiry</div>
    <h2 style="margin-top:8px;">What would you like to understand?</h2>
    <p>Ask a question grounded in the document you uploaded.</p>
    """,
    unsafe_allow_html=True,
)

with st.form("research_question_form"):
    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: What does this document explain? "
            "Summarize the main findings..."
        ),
        height=100,
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "✦  Examine the evidence",
        use_container_width=True,
    )


# --------------------------------------------------
# RETRIEVE, VERIFY AND ANSWER
# --------------------------------------------------

if submitted:
    if not question.strip():
        st.warning("Please enter a question before continuing.")

    else:
        try:
            with st.spinner("Searching your document..."):
                results = search_stored_chunks(
                    question,
                    document_name=document_id,
                    top_k=5,
                )

            if not results:
                st.warning(
                    "No relevant passages were found in this document."
                )

            else:
                with st.spinner(
                    "Examining the evidence and preparing your answer..."
                ):
                    answer = generate_answer(question, results)

                st.markdown(
                    '<div class="gold-line"></div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    """
                    <div class="eyebrow">Research findings</div>
                    <h2>Your answer</h2>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="lux-card">',
                    unsafe_allow_html=True,
                )
                st.markdown(answer)
                st.markdown("</div>", unsafe_allow_html=True)

                source_pages = sorted(
                    {
                        result.get("page", 0)
                        for result in results
                        if result.get("page", 0) > 0
                    }
                )

                if source_pages:
                    page_labels = ", ".join(map(str, source_pages))

                    st.markdown(
                        f"""
                        <div class="small-label">
                            Retrieved PDF pages: {page_labels}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    """
                    <div class="gold-line"></div>
                    <div class="eyebrow">Source references</div>
                    <h3>Supporting evidence</h3>
                    <p>
                        Explore the passages retrieved from your document.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                for index, result in enumerate(results, start=1):
                    page_number = result.get("page", 0)

                    if page_number:
                        source_label = f"Page {page_number}"
                    else:
                        source_label = "Page unavailable"

                    with st.expander(
                        f"Source {index}  ·  {source_label}"
                    ):
                        st.markdown(
                            f"""
                            <div class="source-reference">
                                Document reference · {source_label}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.write(result["chunk"])

                        score = result.get("score")

                        if score is not None:
                            similarity_percentage = score * 100

                            st.caption(
                                f"Semantic similarity: {similarity_percentage:.1f}% "
                                "(retrieval relevance, not answer confidence)"
                            )

        except Exception as error:
            st.error(f"Question processing failed: {error}")


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True,
)
st.markdown("### How it works")

step_columns = st.columns(4)

steps = [
    ("1", "Upload", "Add your PDF"),
    ("2", "Search", "Find relevant passages"),
    ("3", "Verify", "Check supporting evidence"),
    ("4", "Understand", "Read the answer and sources"),
]

for column, (number, title, description) in zip(step_columns, steps):
    with column:
        st.markdown(
            f"""
            <div style="margin:12px 0 25px;">
                <div class="step-number">{number}</div>
                <div class="document-title" style="margin-top:12px;">
                    {title}
                </div>
                <div class="feature-description" style="margin-top:5px;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        NEURALMIND AI &nbsp; · &nbsp; PRIVATE &nbsp; · &nbsp;
        LOCAL &nbsp; · &nbsp; YOUR DOCUMENTS, YOUR CONTROL
        <div style="
            margin-top: 12px;
            color: #C5A56A;
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 11px;
            letter-spacing: 1.5px;
            text-transform: lowercase;
        ">
            by mhd adhil
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
