import PyPDF2
import io
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.embeddings import get_vector_store


def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file object."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def process_pdfs(uploaded_files) -> tuple:
    """
    Process multiple PDFs:
    1. Extract text
    2. Split into chunks
    3. Build vector store
    Returns: (vector_store, total_chunk_count)
    """
    all_chunks = []
    all_metadatas = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        chunks = splitter.split_text(text)
        all_chunks.extend(chunks)
        # Store filename as metadata for each chunk
        all_metadatas.extend([{"source": file.name}] * len(chunks))

    vector_store = get_vector_store(all_chunks, all_metadatas)
    return vector_store, len(all_chunks)
