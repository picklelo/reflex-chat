"""A custom component for a chat interface."""

import reflex as rx


class Chat(rx.ComponentState):
    """A chat component with state."""

    # The full chat history, in the OpenAI format.
    messages2: list[dict[str, str]] = [
        {
            "role": "system",
            "content": "You are a friendly chatbot named Reflex. Respond in markdown.",
        }
    ]

    # Whether we are processing a message.
    processing: bool = False

    @rx.var
    def messages(self) -> list[dict[str, str]]:
        """Return the chat history including the last submitted user message.

        Returns:
            The chat history as a list of dictionaries.
        """
        # Convert to a list before sending.
        return self.get_value(self.messages2)

    @classmethod
    def create(self, process, **props):
        component = super().create(**props)
        component.State.process = process
        return component

    @classmethod
    def get_id(cls):
        return f"chatbox-{cls.get_full_name()}"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.vstack(
            rx.box(
                rx.logo(),
                justify="left",
                background_color=rx.color("accent", 4),
                width="100%",
            ),
            rx.spacer(),
            rx.vstack(
                rx.box(
                    rx.foreach(
                        cls.messages, lambda message, i: chat_bubble(message, i)
                    ),
                    id=f"chatbox-{cls.get_full_name()}",
                    overflow="auto",
                    width="100%",
                    padding_bottom="2em",
                ),
                rx.spacer(),
                action_bar(cls),
                padding=props.pop("padding", "1em"),
                background_color=props.pop("background_color", rx.color("mauve", 1)),
                border=props.pop("border", f"1px solid {rx.color('mauve', 4)}"),
                height="100%",
                width="100%",
                **props,
            ),
            spacing="0",
            height="100%",
            width="100%",
            align="start",
        )

    def scroll_to_bottom(self):
        return rx.call_script(
            f"""
    var element = document.getElementById({f"chatbox-{self.get_full_name()}"}');
    element.scrollTop = element.scrollHeight;
"""
        )

    async def process_message(self):
        async for value in self.process():
            yield value

        self.processing = False

        # Scroll to the last message.
        yield self.scroll_to_bottom()

    def submit_message(self, form_data: dict[str, str]):
        # Get the message from the form
        message = form_data[self.__class__.__name__]

        # Check if the message is empty
        if message == "":
            return

        # Add the message to the list of messages.
        self.messages2.append({"role": "user", "content": message})
        self.messages2.append({"role": "assistant", "content": ""})
        self.processing = True
        yield self.scroll_to_bottom()
        yield type(self).process_message

    @rx.var
    def last_user_message(self) -> str:
        """Return the last submitted user message.

        Returns:
            The last submitted user message.
        """
        for message in reversed(self.messages2):
            if message["role"] == "user":
                return message["content"]
        return ""

    def append_to_response(self, answer: str):
        """Append to the last answer in the chat history.

        Args:
            answer: The answer to add to the chat history.
        """
        self.messages2[-1]["content"] += answer or ""


def chat_bubble(message: str, idx: int = 0) -> rx.Component:
    """Display a single chat bubble.

    Args:
        message: The message to display.

    Returns:
        A component displaying the message/answer pair.
    """
    return rx.cond(
        message["role"] == "system",
        rx.fragment(),
        rx.box(
            rx.markdown(
                message["content"],
                background_color=rx.cond(
                    message["role"] == "user",
                    rx.color("mauve", 4),
                    rx.color("accent", 4),
                ),
                color=rx.cond(
                    message["role"] == "user",
                    rx.color("mauve", 12),
                    rx.color("accent", 12),
                ),
                display="inline-block",
                padding_x="1em",
                border_radius="8px",
                max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
            ),
            id=f"message-{idx}",
            text_align=rx.cond(message["role"] == "user", "right", "left"),
            margin_top="1em",
            width="100%",
        ),
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
