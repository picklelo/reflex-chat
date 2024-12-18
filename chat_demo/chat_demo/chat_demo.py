from reflex_chat import api, chat

import reflex as rx


class State(rx.State):
    messages1: list[dict[str, str]] = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help you today?"},
    ]
    messages2: list[dict[str, str]] = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help you today?"},
    ]

    def clear_messages(self):
        self.messages1 = []
        self.messages2 = []

    def trigger_other_submit(self, id: str, message: str):
        if id == chat1.State.get_id():
            yield chat2.State.process_message(message)
        else:
            yield chat1.State.process_message(message)

chat1 = chat(
    process=api.openai(model="gpt-3.5-turbo"), 
    messages=State.messages1,
    on_submit=State.trigger_other_submit,
)
chat2 = chat(process=api.openai(model="gpt-4"), messages=State.messages2, on_submit=State.trigger_other_submit) 

@rx.page()
def index() -> rx.Component:
    return rx.container(
        rx.hstack(
            chat1,
            chat2,
            rx.button("Clear", on_click=State.clear_messages),
            height="100vh",
        ),
        size="4",
    )


app = rx.App()
