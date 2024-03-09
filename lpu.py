from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from langchain.chains import LLMChain  # Update with the correct import based on your langchain package
from langchain.prompts import PromptTemplate  # Update with the correct import based on your langchain package
#rom langchain_core.prompts import ChatPromptTemplate  # Uncomment if actually used
from langchain_groq import ChatGroq  # Update with the correct import based on your langchain package

class UserRequest(BaseModel):
    query: str
    content: str

app = FastAPI()

llm = ChatGroq(groq_api_key="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", model_name='mixtral-8x7b-32768')

@app.post("/route/")
async def process_request(user_request: UserRequest): 
    query = user_request.query
    content = user_request.content

    prompt_template = """ You are a professional recruiter who specializes in cultivating talent, you are very knowledgable about all types of jobs. Answer the question
    based on the context below.
    
    Context: {content}
    

    Question: {query}
    """

# Define the prompt structure
    prompt = PromptTemplate(
    input_variables=["content", "query"],  
    template=prompt_template,
)


    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Pass the context and question to the Langchain chain
    result_chain = llm_chain.invoke({"content": content, "query": query})

    return result_chain

    if __name__ == "__main__":
    uvicorn.run(app)
