"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config

import os
import reflex as rx
from reflex_chat import chat
from openai import OpenAI


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
        messages=chat.chat_history(),
        stream=True,
    )

    # Stream the results, yielding after every word.
    for item in session:
        if hasattr(item.choices[0].delta, "content"):
            answer_text = item.choices[0].delta.content
            chat.append_to_chat_history(answer_text)
            yield


def index() -> rx.Component:
    return rx.box(
        chat(process=process),
        width="100vw",
        height="100vh",
    )


# Add state and page to the app.
app = rx.App(theme=rx.theme(accent_color="purple"))
app.add_page(index)
