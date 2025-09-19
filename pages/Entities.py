import reflex as rx
import pages.Login
from packages.ApiRequests import ApiRequests
from packages.UiSettings import SettingsState

class EntityDetails(rx.Model, table=True):
    code: str
    type: str
    firstConstant: str
    secondConstant: str
    thirdConstant: str

class EntitiesState(rx.State):
    api_url = ""
    entities = []
    available_entities = []
    entitiesDetails: list[EntityDetails] = []
    user_name = ""

    @rx.event
    async def on_load(self):
        self.api_url = SettingsState.api_url
        settings = await self.get_state(pages.Login.LoginState)
        self.user_name = settings.user_name
        self.entities = ApiRequests(self.api_url).get_entities_assigned_to_user(self.user_name).json()
        self.entitiesDetails = []
        for entity in self.entities:
            self.entitiesDetails.append(ApiRequests(self.api_url).get_entity_details(entity).json()[0])
        self.available_entities = ApiRequests(self.api_url).get_entities().json()
        self.available_entities.append("Select Entity")
        if not settings.logged_in:
            return rx.redirect("/login")

    @rx.event
    def navigate_home(self):
        return rx.redirect("/")

    @rx.event
    def navigate_entities(self):
        return rx.redirect("/entities")

    @rx.event
    def handle_submit(self, form_data):
        if form_data["entity"] in self.available_entities:
            ApiRequests(self.api_url).connect_user_entity(self.user_name, form_data["entity"])
        return rx.redirect("/entities")

    @rx.event
    async def logoff(self):
        settings = await self.get_state(pages.Login.LoginState)
        settings.logged_in = False
        return rx.redirect("/login")
        
def show_record(entitiesDetails: EntityDetails):
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.cell(entitiesDetails[0]),
        rx.table.cell(entitiesDetails[1]),
        rx.table.cell(entitiesDetails[2]),
        rx.table.cell(entitiesDetails[3]),
        rx.table.cell(entitiesDetails[4]),
    )
            
@rx.page(route="/entities", on_load=EntitiesState.on_load)
def entities_page():
    return rx.fragment(
                rx.hstack(
                    rx.drawer.root(
                        rx.drawer.trigger(
                            rx.image(
                                src="/menu.png",
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
                                        style={
                                            "width":"10vw"
                                        },
                                    ),
                                    rx.button(
                                        "Manage Entities",
                                        on_click=EntitiesState.navigate_entities,
                                        color_scheme="purple",
                                        disabled=True,
                                        style={
                                            "width":"10vw"
                                        },
                                    ),
                                    rx.drawer.close(
                                        rx.button(
                                            "Close Menu",
                                            color_scheme="purple",
                                            style={
                                                "width":"10vw"
                                            },
                                        )
                                    ),
                                    rx.button(
                                        "Log Off",
                                        on_click=EntitiesState.logoff,
                                        color_scheme="purple",
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
                                        rx.table.column_header_cell("Code"),
                                        rx.table.column_header_cell("Type"),
                                        rx.table.column_header_cell("First Constant"),
                                        rx.table.column_header_cell("Second Constant"),
                                        rx.table.column_header_cell("Third Constant"),
                                    ),
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        EntitiesState.entitiesDetails, show_record
                                    )
                                ),
                                width="100%",
                            ),
                            rx.card(
                                rx.form(
                                    rx.hstack(
                                        rx.button(
                                            "Add Entity", type='submit'
                                        ),
                                        rx.select(
                                            EntitiesState.available_entities,
                                            default_value="Select Entity",
                                            name='entity',
                                            required=True,
                                        ),
                                    ),
                                    on_submit=EntitiesState.handle_submit,
                                    reset_on_submit=True,
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                ),
            )