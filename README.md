# Chat Component

A Reflex custom component chat.

## Installation

```bash
pip install reflex-chat
```

## Usage

Import the `chat` component to your code. The `chat` component takes a `process` function that will be called every time the user submits a question on the chat box. To achieve the streaming effect, the `process` function should be an async function that yields after appending parts of the streamed response. See the code example below.

```python
from reflex_chat import chat
from openai import OpenAI


class State(rx.State):


async def process(chat):
    """Get the response from the API.

    Args:
        form_data: A dict with the current question.
    """
    # Start a new session to answer the question.
    session = OpenAI().chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=chat.chat_history(),
        stream=True,
    )

    # Stream the results, yielding after every word.
    for item in session:
        if hasattr(item.choices[0].delta, "content"):
            answer_text = item.choices[0].delta.content
            chat.append(answer_text)
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
```
