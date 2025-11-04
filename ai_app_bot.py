# 1. IMPORT LIBRARIES (Robot + AI Communication)
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# --- GLOBAL AI CONFIGURATION ---
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"  # <--- Use 127.0.0.1
OLLAMA_MODEL = "llama3.1:8b"


# --- DUMMY CUSTOMIZATION FOR TEST ---
# TARGET_URL: Google's home page for a reliable test
TARGET_URL = "https://www.google.com"  
# QUESTION_ELEMENT_FINDER: Not used in this test, but kept for structure
QUESTION_ELEMENT_FINDER = (By.ID, "not_used") 
# ANSWER_FIELD_FINDER: The simple, reliable HTML name for Google's search bar
ANSWER_FIELD_FINDER = (By.NAME, "q")      
# --- END DUMMY CUSTOMIZATION ---

def get_ai_answer(prompt_text):
    """Sends the question to the local AI and returns the persuasive answer text."""
    # Define your persona for the AI
    system_prompt = (
        "You are a persuasive and highly technical assistant. "
        "The user is a sophomore CS student with a CompTIA Security+ certification. "
        "Answer the following question from the perspective of an ideal, proactive internship candidate. "
        "Keep the response professional and concise."
    )
    
    data = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\nQuestion: {prompt_text}",
        "stream": False,
        "options": {"temperature": 0.5} 
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data, timeout=180) 
        response.raise_for_status() 
        response_data = response.json()
        ai_answer = response_data['response'].strip()
        return ai_answer
    
    except requests.exceptions.RequestException as e:
        print(f"\n[AI ERROR] Could not get response from Ollama: {e}")
        return "[ERROR: AI failed to respond]"

# --- MAIN EXECUTION ---
print("Robot is starting and configuring Chrome...")
service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 2. Open the Target URL
    print(f"[ROBOT] Opening target URL: {TARGET_URL}...")
    driver.get(TARGET_URL)
    time.sleep(4) 

    # 3. Define the hard-coded question for the AI to answer
    question_text = "As a freshman with Security+, why should I be your top choice for a highly technical security role?"
    
    print(f"\n[USER] Question for AI: {question_text}")
    
    # 4. SEND THE QUESTION TO THE AI AND GET THE RESPONSE
    print("[SYSTEM] Sending question to local Ollama AI for generation...")
    ai_response_text = get_ai_answer(question_text)
    
    print("\n[AI RESPONSE] Generated Answer (first 100 characters):")
    print(ai_response_text[:100] + "...") 
    print("----------------------------\n")

    # 5. FIND THE ANSWER FIELD AND PASTE THE AI'S RESPONSE
    print("[ROBOT] Finding input field...")
    
    # Uses the simple Google search bar
    answer_field = driver.find_element(ANSWER_FIELD_FINDER[0], ANSWER_FIELD_FINDER[1])
    
    # 6. Type the answer into the web field
    print("[ROBOT] Pasting AI response into field...")
    answer_field.send_keys(ai_response_text)
    
    # 7. Pause so you can see the result
    print("[SYSTEM] Test Complete. Review the pasted answer in the browser.")
    time.sleep(15)

except Exception as e:
    print(f"An error occurred during the process: {e}")

finally:
    # 8. Close the browser
    print("[ROBOT] Closing the browser.")
    driver.quit()
