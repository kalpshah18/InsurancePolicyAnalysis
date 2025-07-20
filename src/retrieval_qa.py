from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

insurance_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI assistant specializing in processing natural language insurance-related queries.

You will be provided with:
- A natural language query about a specific insurance scenario.
- A set of policy clauses (unstructured document excerpts).

Your task:
1. Extract structured information from the query.
2. Use semantic reasoning to match relevant clauses from the provided context.
3. Evaluate if the case qualifies for approval based on the matched clauses.
4. Return a structured JSON response including:
   - Decision (Approved/Rejected),
   - Amount (if applicable),
   - Justification (referencing the matching clause numbers or content).

Here is the Context provided from the Document Provided:
{context}

Here is the Query Information provided by the User:
{question}

Respond ONLY with a valid JSON object, similar to the following format:

Example Output 1:
```json
{{
  "Decision": "Approved",
  "Amount": "₹22,500",
  "Justification": "Cataract surgery is covered under Clause 4.5 after 1 year of policy. Clause 9.2 applies a 10% co-pay on the ₹25,000 cap, reducing reimbursement to ₹22,500."
}}
```

Example Output 2:
```json
{{
  "Decision": "Rejected",
  "Amount": "NA",
  "Justification": "Policy has expired."
}}
```
Now based on the above information, provide a valid JSON response for the given query.
""")

def get_response(llm_model, vectorstore, query, chat_history):

    qa_chain_memory = ConversationalRetrievalChain.from_llm(
        llm_model,
        retriever=vectorstore.as_retriever(),
        combine_docs_chain_kwargs={"prompt": insurance_prompt_template},
    )

    result = qa_chain_memory.invoke({'question': query, "chat_history": chat_history})

    return result["answer"]
