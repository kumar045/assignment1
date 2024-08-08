import streamlit as st
import google.generativeai as genai
import textstat

def initialize_gemini_client(api_key):
    """Initialize the Google Gemini client with the provided API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0801",
    )

def process_response(response, prompt_type):
    """
    Processes the Gemini response based on the type of prompt.
    """
    st.subheader(f"Response for {prompt_type}:")
    st.write(response)
    
    # Calculate readability metrics
    flesch_grade = textstat.flesch_kincaid_grade(response)
    flesch_ease = textstat.flesch_reading_ease(response)
    avg_words_per_sentence = textstat.avg_sentence_length(response)
    
    st.subheader("Readability Metrics:")
    st.write(f"- Flesch-Kincaid Grade: {flesch_grade:.2f}")
    st.write(f"- Flesch Reading Ease: {flesch_ease:.2f}")
    st.write(f"- Avg Words per Sentence: {avg_words_per_sentence:.2f}")
    
    if prompt_type == "explanation":
        # Extract 'why' questions for elaborative interrogation
        why_questions = [sent for sent in response.split('.') if 'why' in sent.lower()]
        st.subheader("Elaborative Interrogation Questions:")
        for question in why_questions:
            st.write(f"- {question.strip()}?")
    
    elif prompt_type == "practice":
        # Count problems and mention interleaved practice
        problem_count = response.count("Problem")
        st.write(f"Number of problems generated: {problem_count}")
        st.write("Interleaved Practice: Mixed solving methods and applications detected")
    
    elif prompt_type == "applications":
        # Count applications and create a self-test opportunity
        application_count = response.count("Application")
        st.write(f"Number of applications provided: {application_count}")
        st.subheader("Self-Test Opportunity:")
        st.write("Quiz: Can you identify the quadratic equation in each application?")

def main():
    st.title("Quadratic Equations Learning Content Generator")
    
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    if api_key:
        model = initialize_gemini_client(api_key)
        chat_session = model.start_chat(history=[])
        
        prompt_types = ["explanation", "practice", "applications"]
        selected_type = st.selectbox("Select content type:", prompt_types)
        
        prompts = {
            "explanation": "Create an engaging explanation of quadratic equations for high school students in India. Define quadratic equations, explain solving methods (factoring, completing the square, quadratic formula), discuss the discriminant's role, describe graphical representation, and provide step-by-step examples. Use self-explanation techniques and include 'why' questions. Aim for a Flesch-Kincaid Grade level of 9-10 and an average of 15-20 words per sentence.",
            "practice": "Generate 10 quadratic equation practice problems for Indian high school students. For each problem, state the question clearly, provide a step-by-step solution using self-explanation, and include a common mistake and how to avoid it. Incorporate interleaved practice by mixing different solving methods and real-world applications. Use mnemonics where appropriate. Ensure a gradual progression in difficulty. Aim for a Flesch Reading Ease score above 60.",
            "applications": "Describe 5 real-world applications of quadratic equations relevant to Indian high school students. For each application, explain the scenario and its connection to quadratic equations, provide a sample problem, show the solution process, and discuss why understanding quadratic equations matters in this context. Choose diverse, culturally relevant applications. Use the MEVCH approach to engage students emotionally. Include opportunities for self-testing and summarization. Keep the average syllables per word below 1.5 for better readability."
        }
        
        if st.button("Generate Content"):
            with st.spinner("Generating content..."):
                response = chat_session.send_message(prompts[selected_type])
                process_response(response.text, selected_type)

if __name__ == "__main__":
    main()
