# 🛡️ Project Mirage: AI-Powered Active Defense System

**Built for the Build Beyond AI Hackathon**

## 💡 The Problem
Standard cybersecurity systems are strictly reactive: they block an attacker's IP, teaching the attacker how to bypass the firewall while the security team learns nothing. 

## 🚀 The Solution
Project Mirage is an autonomous, self-healing network defense system. Instead of simply blocking malicious queries (like SQL injections), it seamlessly reroutes the attacker into an AI-generated sandbox. 

Using **Google's Gemini 1.5 Flash**, the system dynamically hallucinates fake corporate data (passwords, user records, financial data) in real-time. 
* **For the Attacker:** They believe they have successfully breached the database and waste time extracting fake data.
* **For the Defender:** The system traps the attacker, neutralizing the threat without any performance impact on the actual production database.

## 🛠️ Technology Stack
* **Google Gemini 1.5 Flash:** Acts as the "Illusionist," dynamically generating synthetic JSON payloads to fool attackers.
* **Python & Gradio:** Powers the enterprise SOC (Security Operations Center) dashboard interface.

## ⚙️ How to Run Locally
1. Clone the repository: `git clone https://github.com/yourusername/project-mirage.git`
2. Navigate to the directory: `cd project-mirage`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file in the root directory and add your Google Gemini API key: `GEMINI_API_KEY=your_key_here`
5. Run the app: `python app.py`

## 🧪 Demo Instructions
1. Enter `alice` to simulate a legitimate user. The system returns actual `200 OK` data.
2. Enter `admin' OR 1=1 --` to simulate a SQL injection attack. Watch as the AI instantly intercepts the payload and generates fake user data to trap the attacker.