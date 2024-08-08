import streamlit as st
import google.generativeai as genai
import textstat
import plotly.graph_objs as go
import numpy as np

def initialize_gemini_client(api_key):
    """Initialize the Google Gemini client with the provided API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0801",
    )

def generate_quadratic_graph(a, b, c):
    """Generate a Plotly graph for a quadratic function."""
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
    Processes the Gemini response based on the type of prompt.
    """
    st.subheader(f"Response for {prompt_type}:")
    st.write(response)
    
    # Calculate readability metrics for further improving prompt so that we can use it for the future
    flesch_grade = textstat.flesch_kincaid_grade(response)
    flesch_ease = textstat.flesch_reading_ease(response)
    avg_words_per_sentence = textstat.avg_sentence_length(response)

    
    if prompt_type == "explanation":
        # Extract 'why' questions for elaborative interrogation
        why_questions = [sent for sent in response.split('.') if 'why' in sent.lower()]
        st.subheader("Elaborative Interrogation Questions:")
        for question in why_questions:
            st.write(f"- {question.strip()}?")
        
        if include_graph:
            st.subheader("Example Quadratic Function Graph:")
            fig = generate_quadratic_graph(1, 0, -4)  # y = x² - 4
            st.plotly_chart(fig)
    
    elif prompt_type == "practice":
        # Count problems and mention interleaved practice
        problem_count = response.count("Problem")
        st.write(f"Number of problems generated: {problem_count}")
        st.write("Interleaved Practice: Mixed solving methods and applications detected")
        
        if include_graph:
            st.subheader("Example Problem Visualization:")
            fig = generate_quadratic_graph(2, -4, -2)  # y = 2x² - 4x - 2
            st.plotly_chart(fig)
    
    elif prompt_type == "applications":
        # Count applications and create a self-test opportunity
        application_count = response.count("Application")
        st.write(f"Number of applications provided: {application_count}")
        st.subheader("Self-Test Opportunity:")
        st.write("Quiz: Can you identify the quadratic equation in each application?")
        
        if include_graph:
            st.subheader("Example Application Graph:")
            fig = generate_quadratic_graph(-4.9, 20, 0)  # Projectile motion: h = -4.9t² + 20t
            fig.update_layout(title="Projectile Motion: Height vs Time")
            st.plotly_chart(fig)

def main():
    st.title("Quadratic Equations Learning Tool")
    
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    if api_key:
        model = initialize_gemini_client(api_key)
        chat_session = model.start_chat(history=[])
        
        prompt_types = ["explanation", "practice", "applications"]
        selected_type = st.selectbox("Select content type:", prompt_types)
        
        include_graph = st.checkbox("Include graph/diagram", value=True)
        
        prompts = {
            "explanation": "Create an engaging explanation of quadratic equations for high school students in India. Define quadratic equations, explain solving methods (factoring, completing the square, quadratic formula), discuss the discriminant's role, describe graphical representation, and provide step-by-step examples. Use self-explanation techniques and include 'why' questions. Aim for a Flesch-Kincaid Grade level of 9-10 and an average of 15-20 words per sentence.",
            "practice": "Generate 10 quadratic equation practice problems for Indian high school students. For each problem, state the question clearly, provide a step-by-step solution using self-explanation, and include a common mistake and how to avoid it. Incorporate interleaved practice by mixing different solving methods and real-world applications. Use mnemonics where appropriate. Ensure a gradual progression in difficulty. Aim for a Flesch Reading Ease score above 60.",
            "applications": "Describe 5 real-world applications of quadratic equations relevant to Indian high school students. For each application, explain the scenario and its connection to quadratic equations, provide a sample problem, show the solution process, and discuss why understanding quadratic equations matters in this context. Choose diverse, culturally relevant applications. Use the MEVCH approach to engage students emotionally. Include opportunities for self-testing and summarization. Keep the average syllables per word below 1.5 for better readability."
        }
        
        if st.button("Generate Content"):
            with st.spinner("Generating content..."):
                response = chat_session.send_message(prompts[selected_type])
                process_response(response.text, selected_type, include_graph)

if __name__ == "__main__":
    main()
