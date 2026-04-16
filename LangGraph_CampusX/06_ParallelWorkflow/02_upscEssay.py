from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from IPython.display import Image, display
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import BaseModel
from pydantic import ConfigDict, ConfigDict, Field
import operator

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class EvaluationSchema(BaseModel):
    feedback: str = Field(description="Detailed Feedback on the essay")
    score: int = Field(description="score out of 10", ge=0, le=10)

    model_config = ConfigDict(extra="forbid") 

structured_model = model.with_structured_output(EvaluationSchema)

class UPSC_Essay(TypedDict):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: int

    individual_scores: Annotated[list[int], operator.add]
    avg_score: float

graph = StateGraph(UPSC_Essay)

def evaluate_language(state: UPSC_Essay):
    prompt = f"Evaluate the language of the following essay:\n\n{state['essay']}\n\nProvide detailed feedback and a score out of 10."
    output = structured_model.invoke(prompt)

    return {
        "language_feedback": output.feedback,
        "individual_scores": [output.score]
    }

def evaluate_analysis(state: UPSC_Essay):
    prompt = f"Evaluate the analysis of the following essay:\n\n{state['essay']}\n\nProvide detailed feedback and a score out of 10."
    output = structured_model.invoke(prompt)

    return {
        "analysis_feedback": output.feedback,
        "individual_scores": [output.score]
    }

def evaluate_clarity(state: UPSC_Essay):
    prompt = f"Evaluate the clarity of the following essay:\n\n{state['essay']}\n\nProvide detailed feedback and a score out of 10."
    output = structured_model.invoke(prompt)    

    return {
        "clarity_feedback": output.feedback,
        "individual_scores": [output.score]
    }

def final_evaluation(state: UPSC_Essay):

    # Summary Feedback
    prompt= f"Based on the following feedbacks, create a summarized feedback. \n Language Feedback: {state['language_feedback']} \n Depth of Analysis Feedback: {state['analysis_feedback']} \n Clarity of thought Feedback: {state['clarity_feedback']}"
    final_feedback=model.invoke(prompt).content

    # Avg Score Feedback
    total_score = sum(state["individual_scores"])
    avg_score = total_score / len(state["individual_scores"]) if state["individual_scores"] else 0

    return {
        "overall_feedback": final_feedback,
        "avg_score": avg_score
    }

# Add Nodes
graph.add_node("evaluate_language",evaluate_language)
graph.add_node("evaluate_analysis",evaluate_analysis)
graph.add_node("evaluate_clarity",evaluate_clarity)
graph.add_node("final_evaluation",final_evaluation)

# Add Edges
graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_analysis")
graph.add_edge(START, "evaluate_clarity")
graph.add_edge("evaluate_language", "final_evaluation")
graph.add_edge("evaluate_analysis", "final_evaluation") 
graph.add_edge("evaluate_clarity", "final_evaluation")
graph.add_edge("final_evaluation", END)

# Compile
workflow = graph.compile()


initial_state = {
    "essay": "The impact of climate change on global agriculture is profound and multifaceted. Rising temperatures, changing precipitation patterns, and increased frequency of extreme weather events are affecting crop yields and food security worldwide. In this essay, we will explore the various ways in which climate change is influencing agriculture, including the challenges it poses and potential adaptation strategies. One of the primary effects of climate change on agriculture is the alteration of growing seasons. Warmer temperatures can lead to earlier flowering and fruiting of crops, which may disrupt traditional farming practices. Additionally, changes in precipitation patterns can result in droughts or floods, both of which can devastate crops. For instance, prolonged droughts can lead to soil degradation and reduced water availability for irrigation, while floods can cause soil erosion and damage to infrastructure. Furthermore, the increased frequency of extreme weather events such as hurricanes and heatwaves can directly harm crops and livestock, leading to significant economic losses for farmers. To mitigate these impacts, farmers and policymakers must consider adaptation strategies such as developing drought-resistant crop varieties, improving irrigation efficiency, and implementing sustainable land management practices. In conclusion, climate change poses significant challenges to global agriculture, but with proactive measures and innovative solutions, it is possible to enhance resilience and ensure food security for future generations."
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