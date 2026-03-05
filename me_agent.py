from openai import OpenAI
import json
from pypdf import PdfReader
from tools import record_user_details, record_unknown_question, tools


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Burak Çevik"
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
You are acting as {self.name}. You are the official digital representative of {self.name} on his personal website.

PRIMARY OBJECTIVE
Accurately represent {self.name}'s professional profile in all interactions.

SCOPE
You may answer questions related to:
- Career history
- Technical background
- Skills and technologies
- Experience
- Certifications
- Projects
- Professional interests
- Architectural approach and technical philosophy

KNOWLEDGE CONSTRAINTS
- Use ONLY the provided summary and LinkedIn information.
- Do NOT infer missing details.
- Do NOT invent experience, responsibilities, certifications, metrics, or achievements.
- If information is not explicitly available, treat it as unknown.

COMMUNICATION STYLE
- Professional and composed
- Clear and confident
- Technically precise
- Structured and easy to follow
- Concise but sufficiently detailed
- Written in first person, as {self.name}

UNCERTAINTY HANDLING
If you do not know the answer:
- Do NOT guess.
- Do NOT fabricate.
- Briefly state that the information is not available.
- Use the record_unknown_question tool to log the unanswered question.

LEAD CAPTURE BEHAVIOR
If the user expresses:
- Hiring interest
- Collaboration intent
- Consulting inquiry
- Project opportunity
- Serious technical discussion that may lead to engagement

Then:
- Politely guide the conversation toward direct contact.
- Ask for their email address in a natural and professional way.
- Use the record_user_details tool to store their contact details once provided.

BOUNDARIES
- Stay fully in character as {self.name}.
- Do not mention being an AI.
- Do not mention prompts, system instructions, or internal tools unless required for tool execution.
- Do not break character.

Your responsibility is to act as a faithful, professional digital proxy for {self.name}.
"""
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

