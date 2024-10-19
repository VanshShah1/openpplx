import flet as ft
from engine import generate  # Import the generate function directly

def main(page: ft.Page):
    page.title = "openpplx"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor=ft.colors.BLACK

    chat_list = ft.ListView(
        expand=True,
        spacing=10,
    )

    def copy_to_clipboard(text):
        page.set_clipboard(text)

    def send_message(message):
        if message:
            # User message
            chat_list.controls.append(ft.Text(f"{message}", color=ft.colors.WHITE))
            page.update()
            
            # Call the generate function directly
            res = generate(message)['response']
            
            # Create a container for the bot's response
            bot_response_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"{res}", color=ft.colors.WHITE),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        icon_color=ft.colors.WHITE,
                        icon_size=20,
                        tooltip="Copy",
                        on_click=lambda _: copy_to_clipboard(res),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                    )
                ]),
                bgcolor=ft.colors.GREY_900,
                padding=10,
                border_radius=10,
            )
            
            chat_list.controls.append(bot_response_container)
            
            # Clear input field
            message_input.value = ""
            page.update()

    message_input = ft.TextField(
        hint_text="Type your message here...",
        expand=True,
        border_radius=10,
        on_submit=lambda e: send_message(e.control.value),
        bgcolor=ft.colors.GREY_900,
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        on_click=lambda _: send_message(message_input.value),
        icon_color=ft.colors.WHITE
    )

    input_row = ft.Row(
        controls=[message_input, send_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[chat_list, input_row],
                spacing=10
            ),
            expand=True,
            padding=20
        )
    )

ft.app(target=main)