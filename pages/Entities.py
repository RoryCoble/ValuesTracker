'''Manage Entities page'''
import reflex as rx
import pages.login
from packages.api_requests import ApiRequests
from packages.ui_settings import SettingsState

class EntitiesState(rx.State):
    """State specific to the Manage Entities page"""
    # pylint: disable=inherit-non-class
    api_url = ""
    entities = []
    available_entities = []
    entities_details: list[list] = []
    user_name = ""

    @rx.event
    async def on_load(self):
        """Confirms that the User is logged in or redirects to the login 
        page then gathers the data necessary to populate the page"""
        self.api_url = SettingsState.api_url
        settings = await self.get_state(pages.login.LoginState)
        self.user_name = settings.user_name
        self.entities = ApiRequests(self.api_url).get_entities_assigned_to_user(
            self.user_name).json()
        self.entities_details = []
        for entity in self.entities:
            self.entities_details.append(ApiRequests(self.api_url).get_entity_details(
                entity).json()[0])
        self.available_entities = ApiRequests(self.api_url).get_entities().json()
        self.available_entities.append("Select Entity")
        if not settings.logged_in:
            return rx.redirect("/login")

    @rx.event
    def navigate_home(self):
        """Redirects the User to the Main page"""
        return rx.redirect("/")

    @rx.event
    def navigate_entities(self):
        """Redirects the User to the Manage Entities page"""
        return rx.redirect("/entities")

    @rx.event
    def handle_submit(self, form_data):
        """Takes in the Add Entity information, calls the appropriate api endpoint, 
        then reloads the page"""
        if form_data["entity"] in self.available_entities:
            ApiRequests(self.api_url).connect_user_entity(self.user_name, form_data["entity"])
        return rx.redirect("/entities")

    @rx.event
    async def logoff(self):
        """Removes the User's logged in state and redirects to the Login page"""
        settings = await self.get_state(pages.login.LoginState)
        settings.logged_in = False
        return rx.redirect("/login")

def show_record(entities_detail: list):
    """Shows the Entity details in a table row."""
    return rx.table.row(
        rx.table.cell(entities_detail[0]),
        rx.table.cell(entities_detail[1]),
        rx.table.cell(entities_detail[2]),
        rx.table.cell(entities_detail[3]),
        rx.table.cell(entities_detail[4]),
        custom_attrs = {
            "data-testid" : "entitiesTableRow",
        },
    )

# pylint: disable=not-callable
@rx.page(route="/entities", on_load=EntitiesState.on_load)
def entities_page():
    """
    Creates the Manage Entities page including the navigation menu, 
    the assigned Entity details table, and the form to add additional
    Entities
    """
    return rx.fragment(
                rx.hstack(
                    rx.drawer.root(
                        rx.drawer.trigger(
                            rx.image(
                                src="/menu.png",
                                custom_attrs = {
                                    "data-testid" : "menuButton",
                                },
                            ),
                        ),
                        rx.drawer.overlay(z_index="5"),
                        rx.drawer.portal(
                            rx.drawer.content(
                                rx.vstack(
                                    rx.button(
                                        "Home",
                                        on_click=EntitiesState.navigate_home,
                                        color_scheme="purple",
                                        custom_attrs = {
                                            "data-testid" : "homeButton",
                                        },
                                        style={
                                            "width":"10vw"
                                        },
                                    ),
                                    rx.button(
                                        "Manage Entities",
                                        on_click=EntitiesState.navigate_entities,
                                        color_scheme="purple",
                                        disabled=True,
                                        custom_attrs = {
                                            "data-testid" : "manageEntitiesButton",
                                        },
                                        style={
                                            "width":"10vw"
                                        },
                                    ),
                                    rx.drawer.close(
                                        rx.button(
                                            "Close Menu",
                                            color_scheme="purple",
                                            custom_attrs = {
                                                "data-testid" : "closeButton",
                                            },
                                            style={
                                                "width":"10vw"
                                            },
                                        )
                                    ),
                                    rx.button(
                                        "Log Off",
                                        on_click=EntitiesState.logoff,
                                        color_scheme="purple",
                                        custom_attrs = {
                                            "data-testid" : "logOffButton",
                                        },
                                        style={
                                            "width":"10vw"
                                        },
                                    ),
                                ),
                                top="auto",
                                right="auto",
                                height="100%",
                                width="20em",
                                padding="2em",
                            ),
                            direction="left",
                        ),
                    ),
                    rx.container(
                        rx.vstack(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell(
                                            "Code",
                                            custom_attrs = {
                                                "data-testid" : "codeHeader",
                                            },
                                        ),
                                        rx.table.column_header_cell(
                                            "Type",
                                            custom_attrs = {
                                                "data-testid" : "typeHeader",
                                            },
                                        ),
                                        rx.table.column_header_cell(
                                            "First Constant",
                                            custom_attrs = {
                                                "data-testid" : "firstConstantHeader",
                                            },
                                        ),
                                        rx.table.column_header_cell(
                                            "Second Constant",
                                            custom_attrs = {
                                                "data-testid" : "secondConstantHeader",
                                            },
                                        ),
                                        rx.table.column_header_cell(
                                            "Third Constant",
                                            custom_attrs = {
                                                "data-testid" : "thirdConstantHeader",
                                            },
                                        ),
                                    ),
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        EntitiesState.entities_details, show_record
                                    ),
                                    custom_attrs = {
                                        "data-testid" : "entitiesTableBody",
                                    },
                                ),
                                width="100%",
                                custom_attrs = {
                                    "data-testid" : "entitiesTable",
                                },
                            ),
                            rx.card(
                                rx.form(
                                    rx.hstack(
                                        rx.button(
                                            "Add Entity", 
                                            type='submit',
                                            custom_attrs = {
                                                "data-testid" : "addEntityButton",
                                            },
                                        ),
                                        rx.select(
                                            EntitiesState.available_entities,
                                            default_value="Select Entity",
                                            name='entity',
                                            required=True,
                                            custom_attrs = {
                                                "data-testid" : "entitySelect",
                                            },
                                        ),
                                    ),
                                    on_submit=EntitiesState.handle_submit,
                                    reset_on_submit=True,
                                ),
                            ),
                        ),
                        width="100%",
                        style={"pointer_events": "auto"},
                    ),
                ),
            )
