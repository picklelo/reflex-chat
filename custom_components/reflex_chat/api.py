"""Define common AI API functions."""

import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    print("OpenAI is not installed. Please install it with `pip install openai`.")


def openai(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
):
    """Get the response from the API.

    Args:
        form_data: A dict with the current question.
    """
    async def process(chat):
        # Start a new session to answer the question.
        session = client.chat.completions.create(
            model=model,
            messages=chat.messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            delta = item.choices[0].delta.content
            chat.append_to_response(delta)
            yield

    return process
