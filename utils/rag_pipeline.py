from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from transformers import pipeline


LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


def load_llm():
    pipe = pipeline(
        "text-generation",
        model=LLM_MODEL,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.3,
        repetition_penalty=1.1,
        device=-1
    )
    return HuggingFacePipeline(pipeline=pipe)


PROMPT = PromptTemplate.from_template("""<|system|>
You are a helpful AI assistant. Answer the question using ONLY the context provided.
If the answer is not in the context, say "I couldn't find this in the documents."
Give a short, direct answer. Do NOT repeat the question or the instructions.
</s>
<|user|>
Context:
{context}

Question: {question}
</s>
<|assistant|>""")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def clean_output(text: str) -> str:
    if "<|assistant|>" in text:
        text = text.split("<|assistant|>")[-1]
    for token in ["</s>", "<|user|>", "<|system|>", "<s>"]:
        text = text.replace(token, "")
    if "Question:" in text:
        text = text.split("Question:")[0]
    if "Context:" in text:
        text = text.split("Context:")[0]
    return text.strip()


def get_answer(question: str, vector_store) -> tuple:
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)
    sources = list(set([d.metadata.get("source", "Unknown") for d in docs]))

    llm = load_llm()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    raw = chain.invoke(question)
    answer = clean_output(raw)

    if not answer:
        answer = "I couldn't find a clear answer in the documents."

    return answer, sources