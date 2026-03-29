import os
from groq import Groq  # Changed import
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Client instead of OpenAI
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_treatment_plan(disease_name, confidence):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # ✅ Use supported model
        model_name = "llama-3.1-8b-instant"
        
        prompt = f"""
        You are an expert agricultural advisor. 
        A farmer has uploaded a leaf image and our AI detected:
        - Disease: {disease_name}
        - Confidence: {confidence:.1f}%
        
        Please provide:
        1. ✅ Brief confirmation of the diagnosis
        2. 🌿 One organic/natural remedy
        3. 💊 One chemical treatment (if severe)
        4. 🛡️ One preventive measure for future
        
        Keep responses concise, practical, and farmer-friendly.
        """
        
        response = client.chat.completions.create(
            model=model_name,  # ✅ Updated model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Agent error: {str(e)}"
    
