# Chat Component

A Reflex custom component chat.

## Installation

```bash
pip install reflex-chat
```

## Usage

See the `chat_demo` folder for an example app.

```python
import reflex as rx
from reflex_chat import chat, api

@rx.page()
def index() -> rx.Component:
    return rx.container(
        rx.box(
            chat(process=api.openai()),
            height="100vh",
        ),
        size="2",
    )

app = rx.App()
```

1. Import the `chat` component to your code.

```python
from reflex_chat import chat
```

2. Specify the `process` function that will be called every time the user submits a question on the chat box. The `process` function should be an async function that yields after appending parts of the streamed response.

We have a default `process` function that uses the OpenAI API to get the response. You can use it by importing the `api` module. Over time we will add more `process` functions into the library.

To use the OpenAI API, you need to set the `OPENAI_API_KEY` environment variable. You can specify the mdoel with the `OPENAI_MODEL` environment variable or pass it as an argument to the `api.openai()` function.

```python
chat(process=api.openai(model="gpt-3.5-turbo")),
```

See below on how to specify your own `process` function.

```python

3. Add the `chat` component to your page.

By default the component takes up the full width and height of the parent container. You can specify the width and height of the component by passing the `width` and `height` arguments to the `chat` component.

```python
@rx.page()
def index() -> rx.Component:
    return rx.container(
        rx.box(
            chat(process=api.openai(model="gpt-3.5-turbo")),
            height="100vh",
        ),
        size="2",
    )
```

## Accessing the Chat State

Once you create a chat component, you can access its state through the `chat.State` object.

Get the messages from the chat state.

```python
chat1 = chat()

@rx.page()
def index() -> rx.Component:
    return rx.container(
        # Get the messages through chat1.State.messages.
        rx.text("Total Messages: ", chat1.State.messages.length()),
        rx.hstack(
            chat1,
            height="100vh",
        ),
        # Get the processing state through chat1.State.processing.
        background_color=rx.cond(chat1.State.processing, "gray", "white"),
        size="4",
    )
```

## Specifying your own process function

You can specify your own `process` function that will be called every time the user submits a question on the chat box. The `process` function should be an async function that takes in the current chat state and yields after appending parts of the streamed response.

The OpenAI `process` function is defined as below:

```python
async def process(chat: Chat):
    # Start a new session to answer the question.
    session = client.chat.completions.create(
        model=model,
        # Use chat.get_messages() to get the messages when processing.
        messages=chat.get_messages(),
        stream=True,
    )

    # Stream the results, yielding after every word.
    for item in session:
        delta = item.choices[0].delta.content
        # Append to the last bot message (which defaults as an empty string).
        chat.append_to_response(delta)
        yield

return process
```
