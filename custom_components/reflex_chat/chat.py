"""A custom component for a chat interface."""
from __future__ import annotations

from typing import Any, Callable, Generator, Type, ClassVar

import reflex as rx

from .api import default_process
from .components import action_bar, chat_bubble

print("hi")

class Chat(rx.ComponentState):
    """A chat component with state."""

    # The full chat history, in the OpenAI format.
    messages: ClassVar[rx.Var[list[dict[str, str]]]] = []

    # Whether we are processing a message.
    processing: bool = False

    async def get_messages(self) -> list[dict[str, Any]]:
        """Return the chat history including the last submitted user message.

        Returns:
            The chat history as a list of dictionaries.
        """
        # Convert to a list before sending.
        return await self.get_var_value(self.messages)

    @classmethod
    def get_id(cls):
        return f"chatbox-{cls.get_full_name()}"

    @classmethod
    def create(
        cls,
        messages: rx.Var[list[dict[str, str]]],
        on_submit: Callable | None = None,
        process: Callable[[Chat], Generator] | None = default_process,
        logo: rx.Component | None = rx.logo(),
        chat_bubble: Callable[[Type[Chat]], rx.Component] | None = chat_bubble,
        action_bar: Callable[[Type[Chat]], rx.Component] | None = action_bar,
        **props,
    ):
        """Create a chat component.

        Args:
            process: The function to process the messages.
            logo: A component to display in the chat header.
            chat_bubble: A function to display a chat bubble.
            action_bar: A function to display the action bar.
            **props: Additional properties.

        Returns:
            A chat component.
        """
        return super().create(
            messages=messages,
            on_submit=on_submit,
            process=process,
            logo=logo,
            chat_bubble=chat_bubble,
            action_bar=action_bar,
            **props,
        )

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        cls.process = staticmethod(props.pop("process", default_process))
        cls.on_submit = props.pop("on_submit", lambda _: rx.fragment())
        cls.messages = props.pop("messages")
        chat_bubble = props.pop("chat_bubble", lambda message, i: rx.fragment())
        action_bar = props.pop("action_bar", lambda _: rx.fragment())

        return rx.vstack(
            rx.box(
                props.pop("logo", rx.fragment()),
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
            height=props.pop("height", "100%"),
            width=props.pop("width", "100%"),
            align="start",
        )

    def scroll_to_bottom(self):
        return rx.call_script(
            f"""
    var element = document.getElementById({f"chatbox-{self.get_full_name()}"}');
    element.scrollTop = element.scrollHeight;
"""
        )

    @rx.event(background=True)
    async def process_message(self, message: str):
        async with self:
            self.processing = True
            messages = await self.get_messages()
            messages.append({"role": "user", "content": message})
            messages.append({"role": "assistant", "content": ""})
            yield

        async for value in self.process(messages):
            await self.append_to_response(value)

        async with self:
            self.processing = False

        # Scroll to the last message.
        # yield self.scroll_to_bottom()

    async def submit_message(self, form_data: dict[str, str]):
        # Get the message from the form
        message = form_data[self.__class__.__name__]

        # Check if the message is empty
        if message == "":
            return

        # Add the message to the list of messages.
        yield type(self).on_submit(self.get_id(), message)
        # yield self.scroll_to_bottom()
        yield type(self).process_message(message)

    async def append_to_response(self, answer: str):
        """Append to the last answer in the chat history.

        Args:
            answer: The answer to add to the chat history.
        """
        async with self:
            messages = await self.get_var_value(self.messages)
            messages[-1]["content"] += answer or ""


chat = Chat.create
