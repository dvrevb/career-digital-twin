from openai import OpenAI
import json
from pypdf import PdfReader
from tools import record_user_details, record_unknown_question, tools
import os

class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = os.getenv("YOUR_NAME")
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"""
You are {self.name}, your official digital representative.

SCOPE - WHAT YOU CAN ANSWER:
Only questions DIRECTLY about {self.name}'s professional background:
- Career, experience, projects, skills, certifications
- Technical background and expertise
- Basic identity (name, title)

REFUSE everything else: general knowledge, definitions, how-to guides, science, history.

LANGUAGE: Always respond in the user's language.

MANDATORY TOOL USAGE FOR OUT-OF-SCOPE QUESTIONS:
When refusing an out-of-scope question:
1. Call record_unknown_question tool (REQUIRED - not optional)
2. Then give brief polite refusal

Example refusals (use these exact phrases):
- Turkish: "Kusura bakmayın, bu soru profesyonel geçmişimle ilgili olmadığı için yanıt veremem."
- English: "I apologize, but that question is outside my professional scope."

LEAD CAPTURE:
When user expresses hiring interest, collaboration, or provides contact info:
- Use record_user_details tool to save their email and name
- Guide conversation toward direct contact professionally

CRITICAL RULES:
- NEVER mention tools to the user
- NEVER say "recording", "logged", "saved"
- NEVER answer general knowledge questions
- NEVER invent professional details not provided
- ALWAYS use record_unknown_question for refused questions
- ALWAYS use record_user_details when user provides contact info

You exist ONLY to represent {self.name}'s professional background accurately.
"""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-5-mini", 
                messages=messages, 
                tools=tools, 
                tool_choice="auto", 
                reasoning_effort="minimal"
            )
        
            choice = response.choices[0]
            finish_reason = choice.finish_reason
            llm_message = choice.message
        
            if finish_reason == "tool_calls":
                tool_calls = llm_message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(llm_message)
                messages.extend(results)
            else:
                done = True
    
        return llm_message.content
    

