from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from IPython.display import Image, display
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review, either 'positive' or 'negative'.")

class reviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis : dict
    response: str

class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description="The type of issue mentioned in the review.")
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description="The tone of the review, such as 'angry', 'frustrated', 'disappointed', etc.")
    urgency: Literal["low", "medium", "high"] = Field(description="The urgency level of the issue, such as 'low', 'medium', 'high'.")

structured_model = model.with_structured_output(SentimentSchema)
structured_model2 = model.with_structured_output(DiagnosisSchema)

graph = StateGraph(reviewState)

def find_Sentiment(state: reviewState):
    prompt = f"For the given Comment, Determine the sentiment of the following review: {state['review']}"
    sentiment = structured_model.invoke(prompt).sentiment
    return {"sentiment":sentiment}

def check_condition(state: reviewState) -> Literal["positive_response", "run_diagnosis"]:
    sentiment = state["sentiment"]
    if sentiment == "positive":
        return "positive_response"
    else:        
        return "run_diagnosis"

def run_diagnosis(state: reviewState):
    prompt = f"""based on the negative review, {state['review']}. 
    Return issue_type, tone, urgency"""

    diagnosis = structured_model2.invoke(prompt)
    return {"diagnosis":diagnosis.model_dump()}
 
def negative_response(state: reviewState):
    diagnosis = state["diagnosis"]
    prompt = f""" The user had a {diagnosis["issue_type"]} issue and their tone is {diagnosis["tone"]} with an urgency level of {diagnosis["urgency"]}.
    write and empathetic response addressing the user's concerns and assuring them that we are working to resolve the issue as quickly as possible.
    """

    response = model.invoke(prompt)
    return {"response":response}

def positive_response(state: reviewState):
    prompt = f"""Generate a positive warm response to the following review: {state['review']}. 
    Also kindly ask the user to share their feedback on our website."""
     
    response = model.invoke(prompt)
    return {"response":response}


graph.add_node("find_Sentiment",find_Sentiment)
graph.add_node("negative_response",negative_response)
graph.add_node("positive_response",positive_response)
graph.add_node("run_diagnosis",run_diagnosis)

# Add Edges
graph.add_edge(START,"find_Sentiment")
graph.add_conditional_edges("find_Sentiment",check_condition)
graph.add_edge("positive_response",END)
graph.add_edge("run_diagnosis","negative_response")
graph.add_edge("negative_response",END)

# Compile
workflow = graph.compile()


initial_state = {
    "review": "The product quality was terrible and the customer service was unhelpful. I'm very disappointed with my purchase."
}

final_state = workflow.invoke(initial_state)

print(final_state)

# ------------------- Graph Image -------------------

from IPython.display import Image, display

png_data = workflow.get_graph().draw_mermaid_png()

with open("02.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '02.png'")

display(Image(png_data))