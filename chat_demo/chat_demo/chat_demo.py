import reflex as rx
from reflex_chat import chat, api


chat1 = chat(process=api.openai(model="gpt-3.5-turbo"))
chat2 = chat(process=api.openai(model="gpt-4"))


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
