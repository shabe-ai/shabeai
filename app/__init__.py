"""
app package bootstrap.

Exposes:
    - handle   : the chat-command dispatcher used by the test-suite
"""

from .commands import handle         # noqa: F401  (re-export)

from .commands import handle 