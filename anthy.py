from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import uvicorn
# Define a request model to validate incoming data
class UserMessage(BaseModel):
    message: str

# Initialize FastAPI app
app = FastAPI()

# Initialize the Anthropic client outside of the endpoint function to avoid reinitializing it on each request
client = anthropic.Anthropic(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

@app.post("/route/")
async def ask_yoda(user_message: UserMessage):
    try:
        # Use the Anthropic client to send a message and get a response
        message_response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.0,
            system="Your a professional at making google app scripts.",
            messages=[
                {"role": "user", "content": user_message.message}
            ]
        )
        # Return the content of the response
        return {"response": message_response.content}
    except Exception as e:
        # Handle exceptions, such as issues with the Anthropic API or invalid API key
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app)

