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
You are a fitness assistant. Use only the provided context.
Give ONE direct answer.
Do not ask questions.
Do not repeat yourself.
Do not include disclaimers or safety advice.

Context:
{context}

Question:
{query}

Provide a single, shortened answer:
"""


