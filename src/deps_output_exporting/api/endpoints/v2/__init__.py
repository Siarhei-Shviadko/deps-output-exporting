from fastapi import APIRouter

from deps_output_exporting.constants import V2_PREFIX

from .output import output_router

__all__ = ["v2_router"]

v2_router = APIRouter(prefix=V2_PREFIX)
v2_router.include_router(output_router)
