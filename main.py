#Imported all required packages
import streamlit as st
import google.generativeai as genai
import textstat
import plotly.graph_objs as go
import numpy as np

def initialize_gemini_client(api_key):
    """Use the API key to start the Google Gemini tool."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0801",
    )

def generate_quadratic_graph(a, b, c):
    """Make a graph for a Quadratic equation that looks like a U shape."""
    x = np.linspace(-10, 10, 100)
    y = a * x**2 + b * x + c
    
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    fig.update_layout(
        title=f'Quadratic Function: y = {a}x² + {b}x + {c}',
        xaxis_title='x',
        yaxis_title='y'
    )
    return fig

def process_response(response, prompt_type, include_graph):
    """
    Depending on what type of question was asked, show the answer in different ways.
    """
    st.subheader(f"Response for {prompt_type}:")
    st.write(response)
    
    # Check how easy or hard the text is to read. This is one of my research we can store it and use later to improve prompt
    flesch_grade = textstat.flesch_kincaid_grade(response)
    flesch_ease = textstat.flesch_reading_ease(response)
    avg_words_per_sentence = textstat.avg_sentence_length(response)

    
    if prompt_type == "explanation":
        # Find and display "why" oriented questions.
        why_questions = [sent for sent in response.split('.') if 'why' in sent.lower()]
        st.subheader("Questions that ask 'Why':")
        for question in why_questions:
            st.write(f"- {question.strip()}?")
        
        if include_graph:
            st.subheader("Example Graph of a U-shaped Equation:")
            fig = generate_quadratic_graph(1, 0, -4)  # y = x² - 4
            st.plotly_chart(fig)
    
    elif prompt_type == "practice":
        # Count how many problems were made and show mixed practice
        problem_count = response.count("Problem")
        st.write(f"Number of problems created: {problem_count}")
        st.write("Mixed Practice: Different solving methods and applications used")
        
        if include_graph:
            st.subheader("Example Graph of a Math Problem:")
            fig = generate_quadratic_graph(2, -4, -2)  # y = 2x² - 4x - 2
            st.plotly_chart(fig)
    
    elif prompt_type == "applications":
        # Count how many real-world uses were given and ask a self-test question
        application_count = response.count("Application")
        st.write(f"Number of real-world uses explained: {application_count}")
        st.subheader("Self-Test Question:")
        st.write("Quiz: Can you find the quadratic equation in each example?")
        
        if include_graph:
            st.subheader("Example Graph of a Real-World Use:")
            fig = generate_quadratic_graph(-4.9, 20, 0)  # This is Projectile motion: height vs time
            fig.update_layout(title="Projectile Motion: Height vs Time")
            st.plotly_chart(fig)

# This is our main function will call our other functions mentioned above
def main():
    st.title("Quadratic Equations Learning Tool")
    
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    if api_key:
        model = initialize_gemini_client(api_key)
        chat_session = model.start_chat(history=[])
        
        prompt_types = ["explanation", "practice", "applications"]
        selected_type = st.selectbox("Select content type:", prompt_types)
        
        include_graph = st.checkbox("Include graph/diagram", value=True)
        
        # This is our prompts
        prompts = {
            "explanation": "Create an easy-to-understand explanation of quadratic equations for high school students in India. Define quadratic equations, explain how to solve them (factoring, completing the square, quadratic formula), discuss the discriminant's role, describe the graph of the equation, and give step-by-step examples. Use questions that start with 'why'. Aim for a reading level of grades 9-10 and sentences with 15-20 words.",
            "practice": "Create 10 practice problems with quadratic equations for high school students in India. For each problem, clearly state the question, provide a step-by-step solution, and include common mistakes and how to avoid them. Mix different solving methods and real-world applications. Use easy memory tricks. Ensure problems get harder gradually. Aim for easy-to-read text with a Flesch Reading Ease score above 60.",
            "applications": "Describe 5 real-world uses of quadratic equations for high school students in India. For each use, explain the situation and how it connects to quadratic equations, give a sample problem, show how to solve it, and explain why understanding quadratic equations is important. Use diverse and culturally relevant examples. Include a self-test question and summarization. Use simple words for better readability."
        }
        
        if st.button("Generate Content"):
            with st.spinner("Generating content..."):
                response = chat_session.send_message(prompts[selected_type])
                process_response(response.text, selected_type, include_graph)

if __name__ == "__main__":
    main()
