# Chat Component

A Reflex custom component chat.

## Installation

```bash
pip install reflex-chat
```

## Usage

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

## API

The chat component contains all the user interface and state needed for a chat interface. You can create multiple chat components on the same page.



- `processing` (bool): Whether the chat is processing a request.
- `messages` (List[Dict[str, str]]): A list of messages in the chat in the format `{"role": str, "content": str}`.
- `last_user_message` (str): The last message sent by the user.
- `append_to_response` (Callable[[str], None]): 

