import reflex as rx
import pages.Login
import pages.Register
import pages.Entities
from packages.ApiRequests import ApiRequests
from packages.UiSettings import SettingsState
import asyncio
from datetime import datetime

from rxconfig import config

class State(rx.State):
    """The app state."""
    api_url = ""
    user_name = ""
    entities = []
    last_timestamp = datetime.min
    collected_graph_data = []
    single_graph_data = []
    stream = False
    
    @rx.event
    async def on_load(self):
        self.api_url = SettingsState.api_url
        settings = await self.get_state(pages.Login.LoginState)
        if not settings.logged_in:
            return rx.redirect("/login")
        self.user_name = settings.user_name
        self.entities = ApiRequests(self.api_url).get_entities_assigned_to_user(self.user_name).json()
        self.collected_graph_data = []
        for entity in self.entities:
            self.collected_graph_data.append(ApiRequests(self.api_url).get_historical_values(entity).json())
        self.last_timestamp = datetime.now()

    @rx.event(background=True)
    async def start_stream(self):
        async with self:
            self.stream = True
        while self.stream:
            async with self:
                i=0
                for entity in self.entities:
                    new_data = ApiRequests(self.api_url).get_new_values(entity, self.last_timestamp).json()
                    self.collected_graph_data[i].extend(new_data)
                    i+=1
                self.last_timestamp = datetime.now()
            await asyncio.sleep(10)

    def stop_stream(self):
        self.stream = False
            
    @rx.event
    def navigate_home(self):
        return rx.redirect("/")

    @rx.event
    def navigate_entities(self):
        return rx.redirect("/entities")

    @rx.event
    async def logoff(self):
        settings = await self.get_state(pages.Login.LoginState)
        settings.logged_in = False
        self.stream = False
        return rx.redirect("/login")

def build_graph(entity, index):
    return rx.card(
        rx.vstack(
            rx.heading(
                entity,
                custom_attrs = {
                    "data-testid" : f"{entity}-Header",
                },
            ),
            rx.recharts.line_chart(
                rx.recharts.line(
                    data_key="value",
                    type_="monotone",
                    stroke="#9456D6",
                    dot={
                        "stroke": "#9456D6", 
                        "fill": rx.color("accent", 4)
                    },
                ),
                rx.recharts.x_axis(data_key="timestamp"),
                rx.recharts.y_axis(),
                rx.recharts.graphing_tooltip(),
                data=State.collected_graph_data[index],
                height=200,
                width='100%',
                margin={
                    "top": 20,
                    "right": 20,
                    "left": 20,
                    "bottom": 20,
                },
                custom_attrs = {
                    "data-testid" : f"{entity}-Graph",
                },
            ),
        ),
        style={
            "width":"60vw"
        }
    )
      
@rx.page(on_load=State.on_load)
def index():
    # Welcome Page (Index)
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
                                    on_click=State.navigate_home,
                                    color_scheme="purple",
                                    disabled=True,
                                    custom_attrs = {
                                        "data-testid" : "homeButton",
                                    },
                                    style={
                                        "width":"10vw"
                                    },
                                ),
                                rx.button(
                                    "Manage Entities",
                                    on_click=State.navigate_entities,
                                    color_scheme="purple",
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
                                    on_click=State.logoff,
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
                        rx.heading(
                            "Entity Tracker",
                            custom_attrs = {
                                "data-testid" : "pageTitle",
                            },
                        ),
                        rx.divider(),
                        rx.vstack(
                            rx.foreach(
                                State.entities,
                                lambda entity, index: build_graph(
                                    entity, index
                                ),
                            ),
                            on_mount=State.start_stream,
                            on_unmount=State.stop_stream,
                        ),
                    ),
                ),
            ),
        )

app = rx.App()
app.add_page(index)
app.add_page(pages.Login.login_page, title = 'Login')
app.add_page(pages.Register.register_page, title = 'Register')
app.add_page(pages.Entities.entities_page, title = 'Manage Entities')