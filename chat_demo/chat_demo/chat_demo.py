import reflex as rx
from reflex_chat import chat, api


chat2 = chat(
    process=api.openai(model="gpt-4"),
    initial_messages=[{"role": "system", "content": "Reply sarcastically only."}],
)
chat1 = chat(process=api.openai(model="gpt-3.5-turbo"))


@rx.page()
def index() -> rx.Component:
    return rx.container(
        rx.hstack(
            chat1,
            chat2,
            height="100vh",
        ),
        size="4",
    )


app = rx.App()
