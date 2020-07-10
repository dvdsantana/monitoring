# Entry point for the application.
from . import app  # For application discovery by the 'flask' command.
from . import jwt  # For JWT initializing
from . import views  # For import side-effects of setting up routes.
