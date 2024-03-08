"""Reflex custom component Chat."""

from typing import ClassVar

import reflex as rx


class Chat(rx.Base):
    """The app state."""

    # The current message
    current_message: str

    # The full chat history.
    messages: list[dict[str, str]] = [{
        "role": "system",
        "content": "You are a friendly chatbot named Reflex. Respond in markdown."
    }]

    # Whether we are processing the question.
    processing: bool = False

    # Dynamic creation of per-component State classes
    _instances: ClassVar[int] = 0

    @classmethod
    def create(cls, process, **props) -> rx.Component:
        cls._instances += 1
        return type(
            f"{cls.__name__}_n{cls._instances}", (cls, rx.State), {}
        ).component(process, **props)

    @classmethod
    def component(cls, process, **props) -> rx.Component:
        cls.process = process
        return rx.vstack(
            rx.foreach(cls.messages, chat_bubble),
            action_bar(cls),
            width="100%",
            padding="1em",
            background_color=rx.color("mauve", 1),
            border=f"1px solid {rx.color('mauve', 4)}",
            **props
        )

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data[str(hash(type(self)))]

        # Check if the question is empty
        if question == "":
            return

        async for value in self.process(question):
            yield value

message_style = dict(
    display="inline-block",
    padding_x="1em",
    border_radius="8px",
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
)

def chat_bubble(message: str) -> rx.Component:
    """Display a single chat bubble.

    Args:
        message: The message to display.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.cond(
        message["role"] == "system",
        rx.fragment(),
        rx.box(
            rx.markdown(
                message["content"],
                background_color=rx.cond(message["role"] == "user", rx.color("mauve", 4), rx.color("accent", 4)),
                color=rx.cond(message["role"] == "user", rx.color("mauve", 12), rx.color("accent", 12)),
                **message_style,
            ),
            text_align=rx.cond(message["role"] == "user", "right", "left"),
            margin_top="1em",
            width="100%",
        )
    )


def action_bar(State) -> rx.Component:
    """The action bar to send a new message."""
    return rx.form(
        rx.hstack(
            rx.chakra.input(
                placeholder="Type something...",
                id=str(hash(State)),
                width="100%",
            ),
            rx.spacer(),
            rx.button(
                "Send",
                type="submit",
                size="3",
            ),
            align_items="center",
            width="100%",
        ),
        width="100%",
        on_submit=State.process_question,
        reset_on_submit=True,
    )

chat = Chat.create