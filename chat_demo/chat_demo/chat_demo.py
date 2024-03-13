"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config

import os
import reflex as rx
from reflex_chat import chat
from openai import OpenAI

filename = f"{config.app_name}/{config.app_name}.py"

class State(rx.State):
    pass


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process(chat):
    """Get the response from the API.

    Args:
        form_data: A dict with the current question.
    """
    # Start a new session to answer the question.
    session = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=chat.get_value(chat.messages),
        stream=True,
    )

    # Stream the results, yielding after every word.
    for item in session:
        if hasattr(item.choices[0].delta, "content"):
            answer_text = item.choices[0].delta.content
            # Ensure answer_text is not None before concatenation
            chat.messages[-1]["content"] += answer_text or ""
            yield

def index() -> rx.Component:
    return rx.box(
        chat(process=process),
        width="100vw",
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
