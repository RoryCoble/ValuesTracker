'''Login page'''
import reflex as rx
from packages.api_requests import ApiRequests
from packages.ui_settings import SettingsState

class LoginState(rx.State):
    """Login page and general User login state"""
    # pylint: disable=inherit-non-class
    api_url = ""
    logged_in = False
    user_name = ""

    @rx.event
    async def on_load(self):
        '''On load gets the base api_url'''
        self.api_url = SettingsState.api_url

    @rx.event
    def handle_submit(self, form_data: dict):
        """
        Takes in the Login data and either lets the User into the application
        or displays a banner error indicating the Login failed
        """
        login_result = ApiRequests(self.api_url).login_user(
            form_data["userName"],
            form_data["password"]
        ).json()
        if login_result is True:
            self.logged_in = True
            self.user_name = form_data["userName"]
            return rx.redirect("/")

        return rx.toast(
                "Login Unsuccessful",
                position = "top-center",
                style = {
                    "background-color": "red",
                    "color": "white",
                    "border": "1px solid red",
                    "border-radius": "0.53m",
                }
            )

# pylint: disable=not-callable)
@rx.page(route="/login", on_load=LoginState.on_load)
def login_page():
    """Creates the Login page"""
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                    rx.heading(
                        "Login",
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
                    rx.hstack(
                        rx.button(
                            "Submit", 
                            type="submit",
                            color_scheme="purple",
                            custom_attrs = {
                                "data-testid" : "submitButton",
                            },
                        ),
                        rx.button(
                            "Register", 
                            on_click=rx.redirect("/register"),
                            color_scheme="purple",
                            custom_attrs = {
                                "data-testid" : "registerButton",
                            },
                        ),
                    ),
                    width="100%",
                    justify="center",
                ),
                on_submit=LoginState.handle_submit,
                reset_on_submit=True,
            ),
        ),
        padding_top="30vh",
    )
