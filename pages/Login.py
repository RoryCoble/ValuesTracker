import reflex as rx
from packages.ApiRequests import ApiRequests
from packages.UiSettings import SettingsState

class LoginState(rx.State):
    api_url = ""
    logged_in = False
    user_name = ""

    @rx.event
    async def on_load(self):
        self.api_url = SettingsState.api_url
    
    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        loginResult = ApiRequests(self.api_url).login_user(
            form_data["userName"], 
            form_data["password"]
        ).json()
        if loginResult == True:
            self.logged_in = True
            self.user_name = form_data["userName"]
            return rx.redirect("/")
        else:
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
            
@rx.page(route="/login", on_load=LoginState.on_load)
def login_page():
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
                        rx.center(
                            rx.link(
                                "Register", 
                                on_click=rx.redirect("/register"),
                                custom_attrs = {
                                    "data-testid" : "registerLink",
                                },
                            ),
                            width="100%",
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