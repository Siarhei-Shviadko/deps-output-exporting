from .base import ForbiddenError, NotFoundError

__all__ = ["ProfileNotFound", "PluginProfileEditingForbidden", "BuiltinProfileEditingForbidden"]


class ProfileNotFound(NotFoundError):
    code = "profile_not_found_error"


class PluginProfileEditingForbidden(ForbiddenError):
    code = "plugin_profile_editing_forbidden"


class BuiltinProfileEditingForbidden(ForbiddenError):
    code = "builtin_profile_editing_forbidden"
