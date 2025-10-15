import reflex as rx
from packages.ApiRequests import ApiRequests
from packages.ui_settings import SettingsState

class RegisterState(rx.State):
    api_url = ""

    @rx.event
    async def on_load(self):
        self.api_url = SettingsState.api_url

    @rx.event
    def handle_submit(self, form_data: dict):
        """
        Handles the Registration form submittal and either creates a new 
        User and redirects to the Login page or displays a banner error with the bubbled up
        Error on registration
        """
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
    """Creates the Register page"""
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                    rx.heading(
                        "Register",
                        custom_attrs = {
                            "data-testid" : "pageTitle",
                        },
                    ),
                    rx.input(
                        placeholder="User Name",
                        name="userName",
                        custom_attrs = {
                            "data-testid" : "usernameInput",
                        },
                    ), 
                    rx.input(
                        placeholder="Password",
                        name="password",
                        custom_attrs = {
                            "data-testid" : "passwordInput",
                        },
                    ),
                    rx.input(
                        placeholder="Email",
                        name="email",
                        custom_attrs = {
                            "data-testid" : "emailInput",
                        },
                    ),
                    rx.hstack(
                        rx.button(
                            "Submit", 
                            type="submit",
                            color_scheme="purple",
                            custom_attrs = {
                                "data-testid" : "submitButton",
                            },
                        ),
                        rx.center(
                            rx.link(
                                "Cancel", 
                                on_click=rx.redirect("/login"),
                                custom_attrs = {
                                    "data-testid" : "cancelLink",
                                },
                            ),
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