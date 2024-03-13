"""A custom component for a chat interface."""

from typing import ClassVar

import reflex as rx


class Chat(rx.Base):
    """"""

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
        ).component(process, _id=cls._instances, **props)

    @classmethod
    def component(cls, process, **props) -> rx.Component:
        cls.process = process
        return rx.vstack(
            rx.box(
                rx.foreach(cls.messages, lambda message, i: chat_bubble(message, i)),
                id=f"chatbox-{cls.__name__}",
                overflow="auto",
                width="100%",
                padding_bottom="2em",
            ),
            rx.spacer(),
            action_bar(cls),
            height="100%",
            width="100%",
            padding=props.pop("padding", "1em"),
            background_color=props.pop("background_color", rx.color("mauve", 1)),
            border=props.pop("border", f"1px solid {rx.color('mauve', 4)}"),
            **props
        )

    def scroll_to_bottom(self):
        return rx.call_script(
            f"""
    var element = document.getElementById('chatbox-{type(self).__name__}');
    element.scrollTop = element.scrollHeight;
"""
        )

    async def process_question(self):
        async for value in self.process():
            yield value

        self.processing = False

        # Scroll to the last message.
        yield self.scroll_to_bottom()

    def submit_message(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data[self.__class__.__name__]

        # Check if the question is empty
        if question == "":
            return

        # Add the question to the list of questions.
        self.messages.append({"role": "user", "content": question})
        self.messages.append({"role": "assistant", "content": ""})
        self.processing = True
        yield self.scroll_to_bottom()
        yield type(self).process_question


def chat_bubble(message: str, idx: int = 0) -> rx.Component:
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
                display="inline-block",
                padding_x="1em",
                border_radius="8px",
                max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
            ),
            id=f"message-{idx}",
            text_align=rx.cond(message["role"] == "user", "right", "left"),
            margin_top="1em",
            width="100%",
        )
    )


def action_bar(State) -> rx.Component:
    """The action bar to send a new message."""
    return rx.form(
        rx.hstack(
            rx.input.root(
                rx.input.input(
                    placeholder="Type something...",
                    id=State.__name__,
                ),
                width="100%",
            ),
            rx.spacer(),
            rx.button(
                "Send",
                type="submit",
            ),
            align_items="center",
            width="100%",
        ),
        width="100%",
        on_submit=State.submit_message,
        reset_on_submit=True,
    )

chat = Chat.create
