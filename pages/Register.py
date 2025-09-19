import reflex as rx
from packages.ApiRequests import ApiRequests
from packages.UiSettings import SettingsState

class RegisterState(rx.State):
    api_url = ""

    @rx.event
    async def on_load(self):
        self.api_url = SettingsState.api_url

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        try:
            registerResult = ApiRequests(self.api_url).create_user(
                form_data["userName"], 
                form_data["password"],
                form_data["email"]
            ).json()
            return rx.redirect("/login")
        except Exception as e:
            return rx.toast(
                f"{e}",
                position = "top-center",
                style = {
                    "background-color": "red",
                    "color": "white",
                    "border": "1px solid red",
                    "border-radius": "0.53m",
                },
            )
            
@rx.page(route="/register", on_load=RegisterState.on_load)
def register_page():
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                    rx.heading("Register"),
                    rx.input(
                        placeholder="User Name",
                        name="userName",
                    ), 
                    rx.input(
                        placeholder="Password",
                        name="password",
                    ),
                    rx.input(
                        placeholder="Email",
                        name="email",
                    ),
                    rx.hstack(
                        rx.button(
                            "Submit", 
                            type="submit",
                            color_scheme="purple",
                        ),
                        rx.center(
                            rx.link("Cancel", on_click=rx.redirect("/login")),
                            width="100%",
                        ),
                    ),
                    width="100%", 
                    justify="center",
                ), 
                on_submit=RegisterState.handle_submit, 
                reset_on_submit=True,
            ), 
        ),
        padding_top="30vh",
    )