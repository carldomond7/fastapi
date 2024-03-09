import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import LLMChain  # Update with the correct import based on your langchain package
from langchain.prompts import PromptTemplate  # Update with the correct import based on your langchain package
# from langchain_core.prompts import ChatPromptTemplate  # Uncomment if actually used
from langchain_groq import ChatGroq  # Update with the correct import based on your langchain package

app = FastAPI()

# Make sure to set GROQ_API_KEY in your environment variables
#GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# This class should reflect the structure of the JSON payload you're expecting
class QueryModel(BaseModel):
    QUERY: str
    CONTENT: str

# Langchain and Groq initialization (Modify according to actual usage and initialization requirements)
llm = ChatGroq(groq_api_key="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", model_name='mixtral-8x7b-32768')
prompt_template = """Use the following context to answer the question:

{CONTENT}

Question: {QUERY}
"""

# Define the prompt structure
prompt = PromptTemplate(
    input_variables=["CONTENT", "QUERY"],  
    template=prompt_template,
)

@app.post("/generate-response")
async def generate_response(data: QueryModel):
    # Match the field names with QueryModel
    context = data.CONTENT
    question = data.QUERY
    
    # Prepare the prompt for the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Pass the context and question to the Langchain chain
    result_chain = (
        {"CONTENT": context, "QUERY": question} | llm_chain
    ) 
  
    result = result_chain.invoke()
    
    return result
