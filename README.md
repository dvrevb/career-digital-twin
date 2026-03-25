---
title: career-digital-twin
app_file: app.py
sdk: gradio
sdk_version: 6.8.0
---

[Open the Project](https://huggingface.co/spaces/revbc/career-digital-twin)

# Career Digital Twin

An AI-powered digital representative that accurately represents a professional's career profile, experience, and expertise through natural conversation.

## Overview

This project creates an intelligent chatbot that serves as your official digital representative on your personal website. It engages visitors in professional conversations about your career, skills, technical background, and experience while maintaining strict boundaries on what information it shares.

## Features

- **Accurate Professional Representation**: Answers questions about career history, technical skills, certifications, and projects
- **Knowledge Constraints**: Only uses provided information - never invents or infers missing details
- **Lead Capture**: Naturally collects contact information from interested recruiters, collaborators, or clients
- **Unknown Question Tracking**: Logs questions it cannot answer for future knowledge base improvements
- **First-Person Interaction**: Communicates as you, maintaining a professional and authentic voice

## Installation

### Using uv
```bash
git clone https://github.com/dvrevb/career-digital-twin.git
cd career-digital-twin
uv sync
uv run app.py
```

### Using conda
```bash
git clone https://github.com/dvrevb/career-digital-twin.git
cd career-digital-twin
conda create -n career-twin python=3.12
conda activate career-twin
pip install -r requirements.txt
python app.py
```

### Using pip
```bash
git clone https://github.com/dvrevb/career-digital-twin.git
cd career-digital-twin
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Configuration

### 1. Set Up Your Profile

Create a `.env` file in the project root:

```env
# Your Information
YOUR_NAME=John Doe

# OpenAI API Key (for the LLM)
OPENAI_API_KEY=your-api-key-here

# Pushover (for notifications and logging)
PUSHOVER_USER_KEY=your-pushover-user-key
PUSHOVER_API_TOKEN=your-pushover-api-token
```

### 2. Prepare Your Knowledge Base

Place these files in the project root:

- **`linkedin.pdf`**: Your LinkedIn profile exported as PDF
- **`summary.txt`**: Your professional summary and additional context

These files serve as the static knowledge base for the digital twin.

### 3. Set Up Pushover Notifications

1. **Sign up** at https://pushover.net/ (free trial, then ~$5 one-time)
2. **Get User Key**: Found on your Pushover dashboard after login
3. **Create Application**: 
   - Go to "Create an Application/API Token"
   - Name it (e.g., "Career Digital Twin")
   - Copy the API Token
4. **Add to .env**: Both keys go in your `.env` file

Now you'll receive instant mobile notifications when:
- Someone expresses hiring/collaboration interest
- The bot encounters a question it can't answer

## System Behavior

### What It Does

✅ Answers questions about your career accurately  
✅ Maintains professional tone in first person  
✅ Captures leads from interested parties  
✅ Logs unknown questions for improvement  
✅ Stays strictly within provided knowledge  

### What It Doesn't Do

❌ Invent or guess missing information  
❌ Reveal it's an AI (stays in character)  
❌ Answer questions outside professional scope  
❌ Share personal/private information not in knowledge base  

### Lead Capture Triggers

The system will politely ask for contact information when users express:

- Hiring interest
- Collaboration opportunities
- Consulting inquiries
- Project opportunities
- Serious technical discussions

**Example interaction:**
```
User: "I'd like to discuss a potential consulting opportunity"
Bot: "I'd be happy to discuss this further. Could you share your 
      email address so we can continue the conversation directly?"
```

## Project Structure

```
career-digital-twin/
├── app.py                 # Main Gradio application
├── me_agent.py        # Chat logic and LLM integration
├── tools.py              # Lead capture & question logging tools
├── me/                   # Your personal data (not committed to public repos)
│   ├── linkedin.pdf      # LinkedIn profile export
│   └── summary.txt       # Professional summary
├── pyproject.toml        # uv/pip dependencies
├── uv.lock              # Locked dependency versions
├── requirements.txt      # pip/conda compatibility
├── .env                 # Configuration (not committed)
├── .gitignore
└── README.md
```

## Usage

### Running the App

```bash
# Start the Gradio interface
uv run app.py

# The app will launch at http://localhost:7860
```

### Customization

#### Modify System Prompt

Edit the system prompt in `me_agent.py` to adjust:
- Communication style
- Boundary rules
- Lead capture behavior
- Tone and personality

#### Add Custom Tools

The current implementation uses Pushover for real-time notifications:

**Existing tools in `tools.py`:**
- `record_user_details`: Captures contact info and sends Pushover notification
- `record_unknown_question`: Logs unanswered questions via Pushover

**Pushover Notifications Include:**
- New lead contact information
- Questions the bot couldn't answer
- Timestamps and context

**Get Pushover credentials:**
1. Sign up at https://pushover.net/
2. Get your User Key from the dashboard
3. Create an application to get API Token
4. Add both to your `.env` file

You can extend these tools or add new ones for:
- Scheduling meetings
- Document sharing
- Analytics tracking

## Technology Stack

- **Gradio 6.8.0**: Web UI framework
- **OpenAI API**: Language model for conversations
- **Pushover**: Real-time notifications for leads and logging
- **Python-dotenv**: Environment configuration
- **pypdf**: PDF processing (for LinkedIn profile parsing)
- **uv**: Fast Python package manager

## Development

### Adding Dependencies

```bash
# Add new packages
uv add package-name

# Update requirements.txt
uv pip compile pyproject.toml -o requirements.txt
```

### Testing

```bash
# Run tests (if you add them)
uv run pytest

# Type checking
uv run mypy app.py
```

## Deployment

### Deploy to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Push your code:
```bash
git remote add hf https://huggingface.co/spaces/your-username/career-twin
git push hf main
```
3. Add environment variables in Space settings → Secrets:
   - `OPENAI_API_KEY`
   - `PUSHOVER_USER_KEY`
   - `PUSHOVER_API_TOKEN`
   - `YOUR_NAME`

### Deploy to Hugging Face Spaces/2

```bash

cd career-digital-twin
gradio deploy
# Then follow the instructions

```

### Deploy to Cloud (Railway, Render, etc.)

1. Connect your GitHub repo
2. Set environment variables in the platform
3. Deploy!

## Privacy & Data Handling

- **Contact Information**: Sent via Pushover notifications when captured
- **Unknown Questions**: Logged via Pushover for knowledge base improvements
- **Conversations**: Not persisted by default (ephemeral)
- **Notifications**: Delivered securely through Pushover's encrypted service
- **Personal Data**: `linkedin.pdf` and `summary.txt` should NOT be committed to public repos (add to `.gitignore` if repo is public)

**Add to .gitignore for public repos:**
```
linkedin.pdf
summary.txt
.env
```

## Roadmap

### Version 1.0 (Current) - Static Knowledge Base
- ✅ Basic chat interface with Gradio
- ✅ Static knowledge from `linkedin.pdf` and `summary.txt`
- ✅ Lead capture functionality
- ✅ Unknown question logging

### Version 2.0 - RAG Implementation
- 🔄 Implement Retrieval-Augmented Generation (RAG)
- 🔄 Vector database integration (Pinecone, ChromaDB, or FAISS)
- 🔄 Semantic search over knowledge base
- 🔄 Dynamic context retrieval for more accurate responses

### Version 3.0 - Response Quality Control
- 📅 Add LLM Judge/Reviewer layer
- 📅 Validate response accuracy before sending
- 📅 Multi-step reasoning for complex queries
- 📅 Confidence scoring for answers

### Future Enhancements
- 📅 Multi-modal support (images, documents)
- 📅 Conversation memory and context
- 📅 Analytics dashboard for visitor insights
- 📅 A/B testing for different response strategies

**Note**: Remember to update your knowledge base regularly to keep your digital twin accurate and current!
