Project Compass: Dynamic Project Summarizer
Overview
Project Compass is a generative AI-powered web application that addresses the common problem of fragmented knowledge and information overload in professional settings. This tool transforms unstructured project data—like meeting notes, Slack conversations, or long-form documents—into a clear, structured, and visually compelling overview.

It helps teams by:

Summarizing key information like project goals, risks, and decisions.

Generating dynamic visualizations like a Gantt chart to track milestones and progress.

Reducing friction for new team members and stakeholders who need to get up to speed quickly.

This prototype was built using Python, Streamlit, LangChain, and Google's Gemini API.

Features
AI-Powered Summarization: Converts raw text into a concise project summary.

Milestone Visualization: Automatically extracts project milestones and creates an interactive Gantt chart.

Key Insights Extraction: Identifies and displays a list of project risks and major decisions.

Secure API Handling: Uses environment variables to securely manage API keys.

Demo
Getting Started
Follow these steps to get a local copy of the project up and running.

Prerequisites
Python 3.9+ installed on your system.

A Google Gemini API key. You can get one for free at Google AI Studio.

Setup
Clone the Repository:

git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

Create and Activate a Virtual Environment:
This isolates the project's dependencies from your system's global Python installation.

Windows (Command Prompt):

python -m venv venv
.\venv\Scripts\activate

Mac/Linux:

python3 -m venv venv
source venv/bin/activate

Install Required Packages:
With your virtual environment active, install the project's dependencies using the provided requirements.txt file.

pip install -r requirements.txt

Set Your API Key:
The application needs your Gemini API key to function. The safest way to provide it is through an environment variable.

Create a copy of the .env.example file and rename it to .env.

Open the new .env file and replace the placeholder with your actual API key.

Note: The application is configured to read this file automatically, so you do not need to run a set or export command.

Run the Application:
Once your virtual environment is active and your .env file is set up, you can launch the Streamlit app.

streamlit run app.py

Your application will open in your default web browser, and you're ready to go!
