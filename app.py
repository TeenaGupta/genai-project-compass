# app.py (using Streamlit)

import streamlit as st
import json
import plotly.express as px
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
import os
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Model for Structured Output ---
# This defines the exact structure we want from the model,
# which is the most reliable way to get valid JSON.
class Milestone(BaseModel):
    name: str = Field(description="The name of the project milestone.")
    start_date: str = Field(description="The start date of the milestone in YYYY-MM-DD format.")
    end_date: str = Field(description="The end date of the milestone in YYYY-MM-DD format.")
    owner: str = Field(description="The name of the person or team responsible for the milestone.")

class Risk(BaseModel):
    description: str = Field(description="A description of the project risk.")
    severity: str = Field(description="The severity of the risk (e.g., low, medium, high).")
    mitigation: str = Field(description="A plan to mitigate the risk.")

class Decision(BaseModel):
    date: str = Field(description="The date the decision was made in YYYY-MM-DD format.")
    decision: str = Field(description="A description of the key decision.")

class ProjectSummary(BaseModel):
    project_title: Optional[str] = Field(description="The title of the project.")
    summary: Optional[str] = Field(description="A concise summary of the project goals.")
    milestones: List[Milestone] = Field(description="A list of key project milestones.")
    risks: List[Risk] = Field(description="A list of identified project risks.")
    decisions: List[Decision] = Field(description="A list of key project decisions.")

# --- AUTHENTICATION & MODEL SETUP ---
google_api_key = os.environ.get("GOOGLE_API_KEY")

if not google_api_key:
    st.error("Google API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")
else:
    # Use the structured output method for reliable JSON.
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=google_api_key).with_structured_output(ProjectSummary)

    # The prompt template to get structured JSON output
    # The prompt can now be much simpler because the model is already
    # constrained by the Pydantic schema.
    prompt_template = """
    You are a project manager's assistant. Your task is to extract key project information from the following unstructured text.

    Text to analyze:
    "{text}"
    """
    chat_prompt = ChatPromptTemplate.from_template(prompt_template)

    # Streamlit App UI
    st.title("Project Compass: Dynamic Project Summarizer")
    st.markdown("Paste your project notes, meeting minutes, or messages below to get a real-time summary.")

    user_input = st.text_area("Paste Project Data Here:", height=300)

    if st.button("Generate Summary & Visualization"):
        if user_input:
            with st.spinner("Processing your project data..."):
                try:
                    chain = chat_prompt | llm
                    project_data = chain.invoke({"text": user_input})
                    
                    # The response is now a Pydantic object, not a JSON string.
                    # We can use its attributes directly.
                    st.header("Project Summary")
                    st.subheader(project_data.project_title or "No Title Found")
                    st.write(project_data.summary or "No summary found.")

                    st.subheader("Key Risks")
                    for risk in project_data.risks:
                        st.write(f"**Description:** {risk.description}")
                        st.write(f"**Severity:** {risk.severity}")
                        st.write(f"**Mitigation:** {risk.mitigation}")
                        st.divider()

                    st.subheader("Key Decisions")
                    for decision in project_data.decisions:
                        st.write(f"**Date:** {decision.date}")
                        st.write(f"**Decision:** {decision.decision}")
                        st.divider()

                    milestones = project_data.milestones
                    if milestones:
                        milestones_list = [m.model_dump() for m in milestones]
                        for m in milestones_list:
                            m['start_date'] = datetime.strptime(m['start_date'], '%Y-%m-%d')
                            m['end_date'] = datetime.strptime(m['end_date'], '%Y-%m-%d')
                        
                        st.subheader("Project Milestones (Gantt Chart)")
                        fig = px.timeline(milestones_list, 
                                         x_start="start_date", 
                                         x_end="end_date", 
                                         y="name", 
                                         color="owner",
                                         title="Project Timeline")
                        st.plotly_chart(fig)
                    else:
                        st.info("No milestones found in the project data to create a timeline.")

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please paste some text to get started.")
