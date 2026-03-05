from dotenv import load_dotenv
import gradio as gr
from me_agent import Me


load_dotenv(override=True)


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat).launch()
    