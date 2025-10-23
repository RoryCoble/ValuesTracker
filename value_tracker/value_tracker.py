'''Main page of Values Tracker'''
import asyncio
from datetime import datetime
import pandas as pd
import reflex as rx
import pages.login
import pages.register
import pages.entities
from packages.api_requests import ApiRequests
from packages.ui_settings import SettingsState

class State(rx.State):
    """The base State of the application"""
    # pylint: disable=inherit-non-class
    api_url = ""
    user_name = ""
    entities = []
    last_count = 0
    collected_graph_data = []
    single_graph_data = []
    stream = False

    @rx.event
    async def on_load(self):
        """Checks that the User is logged in, redirects if not, and loads
        the data necessary to produce the Entity graphs"""
        self.api_url = SettingsState.api_url
        settings = await self.get_state(pages.login.LoginState)
        if not settings.logged_in:
            return rx.redirect("/login")
        self.user_name = settings.user_name
        self.entities = ApiRequests(self.api_url).get_entities_assigned_to_user(
            self.user_name).json()
        self.collected_graph_data = []
        last_count = None
        for entity in self.entities:
            response = ApiRequests(self.api_url).get_historical_values(
                entity).json()
            self.collected_graph_data.append(response)
            last_count = response[-1]['count']
        self.last_count = last_count if last_count is not None else 0

    # pylint: disable=not-callable
    @rx.event(background=True)
    async def start_stream(self):
        """Background function to update the graphs on a 10 second interval"""
        async with self:
            self.stream = True
        while self.stream:
            async with self:
                i=0
                last_count = None
                for entity in self.entities:
                    new_data = ApiRequests(self.api_url).get_new_values(
                        entity, self.last_count).json()
                    self.collected_graph_data[i].extend(new_data)
                    i+=1
                    last_count = new_data[-1]['count']
                self.last_count = last_count if last_count is not None else 0
                i=0
                for data in self.collected_graph_data:
                    df = pd.DataFrame(data)
                    df = df.drop_duplicates()
                    self.collected_graph_data[i] = df.to_dict(orient='records')
                    i+=1
            await asyncio.sleep(70)

    def stop_stream(self):
        """Stops the background task so data isn't being sent to nothing"""
        self.stream = False

    @rx.event
    def navigate_home(self):
        """Redirects the user to the Home page"""
        return rx.redirect("/")

    @rx.event
    def navigate_entities(self):
        """Redirects the user to the Manage Entities page"""
        return rx.redirect("/entities")

    @rx.event
    async def logoff(self):
        """Removes the logged in state from the User and redirects them to the Login page"""
        settings = await self.get_state(pages.login.LoginState)
        settings.logged_in = False
        self.stream = False
        return rx.redirect("/login")

def build_graph(entity, i):
    """
    Creates a line graph for the provided Entity
    Keyword arguments:
    entity -- the Entity to be graphed
    i -- counter variable used to access the data stored in self.collected_graph_data
    """
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
                rx.recharts.x_axis(data_key="count"),
                rx.recharts.y_axis(),
                rx.recharts.graphing_tooltip(),
                data=State.collected_graph_data[i],
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

# pylint: disable=not-callable
@rx.page(on_load=State.on_load)
def index():
    """Defines the main page of the application including the 
    navigation menu and the Entity charts"""
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

# Application setup and connection of the various pages
# pylint: disable=not-callable
app = rx.App()
app.add_page(index)
app.add_page(pages.login.login_page, title = 'Login')
app.add_page(pages.register.register_page, title = 'Register')
app.add_page(pages.entities.entities_page, title = 'Manage Entities')
