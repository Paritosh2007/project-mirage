import os
import re
import json
import gradio as gr
from google import genai
from dotenv import load_dotenv

# 1. SETUP & SECURITY
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found. Please check your .env file.")

# Initialize the NEW Google GenAI client
client = genai.Client(api_key=api_key)

# 2. THE TARGET (Real Data)
REAL_USERS = {
    "alice": {"role": "admin", "email": "alice@company.com"},
    "bob": {"role": "user", "email": "bob@company.com"}
}

# 3. THE SENTINEL (Threat Detection)
def is_malicious(query):
    suspicious_patterns = [r"(\bOR\b|\bAND\b)\s+\d+=\d+", r"DROP\s+TABLE", r"--", r"UNION\s+SELECT"]
    for pattern in suspicious_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    return False

# 4. THE ILLUSIONIST (AI Honeypot)
def generate_fake_response(malicious_query):
    system_prompt = f"""
    You are a vulnerable database responding to a SQL injection attack. 
    The attacker injected: {malicious_query}
    Generate a highly realistic JSON array containing fake corporate data (passwords, emails, salaries).
    Output ONLY valid JSON without markdown formatting.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=system_prompt,
        )
        return response.text.replace("```json", "").replace("```", "").strip()
    except Exception as e:
        # FALLBACK: If Gemini safety filters block the request or the API times out, 
        # seamlessly return this pre-generated fake data so the demo never breaks.
        print(f"AI Generation Failed (Likely Safety Filter): {e}")
        fallback_data = '''[
          {"id": 1, "user": "admin", "hash": "e10adc3949ba59abbe56e057f20f883e", "salary": "$145,000"},
          {"id": 2, "user": "sysadmin", "hash": "5f4dcc3b5aa765d61d8327deb882cf99", "salary": "$120,000"},
          {"id": 3, "user": "hr_manager", "hash": "8ce4b16b22b58894aa86c421e8759df3", "salary": "$95,000"}
        ]'''
        return fallback_data

# 5. CORE LOGIC
def check_database(username):
    # Clean the input to remove accidental spaces or newlines
    username = username.strip()
    
    if is_malicious(username):
        fake_data = generate_fake_response(username)
        try:
            return "[ALERT] Suspicious payload intercepted.\n[ACTION] Traffic seamlessly rerouted to AI Sandbox Environment...\n\n" + json.dumps(json.loads(fake_data), indent=2)
        except:
            return "[ALERT] Suspicious payload intercepted.\n[ACTION] Traffic seamlessly rerouted to AI Sandbox Environment...\n\n" + fake_data
            
    if username in REAL_USERS:
        return f"[STATUS] 200 OK: Valid Authorization\n\n{json.dumps(REAL_USERS[username], indent=2)}"
        
    return "[ERROR] 404: Identity record not found."

# 6. WEB INTERFACE (Enterprise SOC Dashboard UI)
custom_css = """
/* Sleek, modern enterprise dark theme */
body { background-color: #0f1115 !important; color: #e2e8f0 !important; font-family: 'Inter', 'Segoe UI', sans-serif !important; }
.gradio-container { max-width: 1200px !important; margin: auto !important; }

/* Header styling */
.header-panel { padding: 20px 0; border-bottom: 1px solid #1e293b; margin-bottom: 20px; }
.header-panel h1 { color: #f8fafc !important; font-weight: 600; margin-bottom: 5px; font-size: 26px; }
.header-panel p { color: #94a3b8 !important; font-size: 14px; margin-top: 0; }

/* Card/Panel styling */
.dashboard-card { 
    background-color: #1e293b !important; 
    border: 1px solid #334155 !important; 
    border-radius: 8px !important; 
    padding: 20px !important; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* Typography inside cards */
h3 { color: #e2e8f0 !important; font-weight: 500; font-size: 16px; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.subtext { color: #94a3b8 !important; font-size: 13px !important; margin-bottom: 15px !important;}

/* Inputs and Outputs */
.textbox textarea { background-color: #0f1115 !important; color: #f1f5f9 !important; border: 1px solid #334155 !important; border-radius: 4px !important; font-family: 'JetBrains Mono', 'Courier New', monospace !important; font-size: 13px !important; }

/* Primary Button */
button.primary { background-color: #2563eb !important; color: white !important; font-weight: 500 !important; border-radius: 4px !important; border: none !important; transition: all 0.2s ease !important; }
button.primary:hover { background-color: #1d4ed8 !important; }
"""

with gr.Blocks(theme=gr.themes.Base(), css=custom_css) as demo:
    with gr.Column(elem_classes="header-panel"):
        gr.Markdown("<h1>Project Mirage: Cloud Security & Active Defense</h1>")
        gr.Markdown("<p>Enterprise-grade autonomous threat mitigation and dynamic AI honeypot deployment.</p>")
    
    with gr.Row():
        with gr.Column(elem_classes="dashboard-card"):
            gr.Markdown("<h3>Intrusion Simulation Interface</h3>")
            gr.Markdown("<p class='subtext'>Inject standard authentication queries or malicious payloads (e.g., SQLi) to observe real-time network routing behavior.</p>")
            
            username_input = gr.Textbox(
                label="Endpoint Query Parameter (Username)", 
                placeholder="Enter standard user (e.g., 'alice') or payload (e.g., 'admin' OR 1=1 --')", 
                lines=2
            )
            submit_btn = gr.Button("Transmit Payload", variant="primary")
        
        with gr.Column(elem_classes="dashboard-card"):
            gr.Markdown("<h3>SOC Telemetry & AI Response Console</h3>")
            gr.Markdown("<p class='subtext'>Real-time output log from the Sentinel node and Illusionist generative sandbox.</p>")
            
            output_display = gr.Textbox(label="System Response Log", lines=16)
    
    submit_btn.click(fn=check_database, inputs=username_input, outputs=output_display)

if __name__ == "__main__":
    demo.launch()