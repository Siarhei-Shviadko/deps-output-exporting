from fastapi import APIRouter

from deps_output_exporting.constants import V1_PREFIX

from .output import output_router
from .profile import profile_router

__all__ = ["v1_router"]

v1_router = APIRouter(prefix=V1_PREFIX)
v1_router.include_router(profile_router)
v1_router.include_router(output_router)
