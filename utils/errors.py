# Custom errors that enhance readability in the codebase and/or introduce
# extra functionality over the built-in Python and D.PY errors

import discord
from discord.ext.commands.errors import CheckFailure


class DataValidationError(ValueError):
    """
    Raise when a data validator (method performing various checks and operations
    on data) encountered a problem that prevented it from continuing.
    """
    def __init__(self, message: str):
        self.message = message
        super(DataValidationError, self).__init__(message)


class InviteValueError(ValueError):
    """
    Raise when the provided invite was of the correct
    format but did not point to a valid guild.
    """
    def __init__(self, message: str, invite: discord.Invite):
        self.message = message
        self.invite = invite  # The offending invite that caused the error
        super(InviteValueError, self).__init__(message, invite)


class NotStaff(CheckFailure):
    """
    Raise when member runs a command that is restricted to staff
    members only (and optionally restricted to a specific staff role).
    """
    def __init__(self, message: str):
        self.message = message
        super(CheckFailure, self).__init__(message)
