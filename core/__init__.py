"""
core/__init__.py

Initializes the core package for the HR-Automation Agent.
Exposes the primary Google API authentication functions so they can be 
easily imported across the unified application.

Usage example in other files:
    from core import get_service
"""

from .google_auth import get_service, get_google_credentials

# Explicitly define what is exported when using `from core import *`
__all__ = [
    "get_service",
    "get_google_credentials"
]