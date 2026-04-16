"""
ui/__init__.py

Initializes the UI package for the HR-Automation Agent.
Exposes the tab rendering functions so they can be cleanly imported into app.py.
"""

from .offer_tab import render_offer_tab
from .reimburse_tab import render_reimburse_tab

# Explicitly define what is exported when using `from ui import *`
__all__ = [
    "render_offer_tab",
    "render_reimburse_tab"
]