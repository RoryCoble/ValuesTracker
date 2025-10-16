'''Reflex config file for its compiler'''
import reflex as rx

# pylint: disable=not-callable
config = rx.Config(
    app_name="value_tracker",
    plugins=[rx.plugins.SitemapPlugin()],
)
