#Assemble prompt to be sent to LLM
def build_prompt(query: str, retrieved_docs: list):
    context_blocks = []

    for doc, meta in retrieved_docs:
        block = f"""
        [Document]
        Date: {meta.get('date')}
        Type: {meta.get('type')}
        Content:
        {doc}
        """
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    return f"""
You are a fitness assistant. Use ONLY the context below to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""
