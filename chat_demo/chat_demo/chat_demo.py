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

async def process(chat, question: str):
    """Get the response from the API.

    Args:
        form_data: A dict with the current question.
    """
    # Add the question to the list of questions.
    chat.messages.append({"role": "user", "content": question})

    # Set the processing flag.
    chat.processing = True

    # TODO: We need an `rx.scroll_to` function to simplify this.
    yield rx.call_script(f"document.getElementById('message-{len(chat.messages) - 1}').scrollIntoView();")

    # Start a new session to answer the question.
    session = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=chat.get_value(chat.messages),
        stream=True,
    )

    # Add an empty answer to the chat history.
    chat.messages.append({"role": "assistant", "content": ""})
    yield rx.call_script(f"document.getElementById('message-{len(chat.messages) - 1}').scrollIntoView();")

    # Stream the results, yielding after every word.
    for item in session:
        if hasattr(item.choices[0].delta, "content"):
            answer_text = item.choices[0].delta.content
            # Ensure answer_text is not None before concatenation
            chat.messages[-1]["content"] += answer_text or ""
            yield

    # Toggle the processing flag.
    chat.processing = False


def index() -> rx.Component:
    return rx.box(
        chat(process=process),
        rx.el.iframe(src="https://chat.reflex.run", width="100%", height="400px"),
        width="100%",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
