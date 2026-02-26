from aiogram import Router

from .users.start import router as start_router
from .users.help import router as help_router
from .users.echo import router as echo_router
from .users.register import router as register_router
from .groups.modernator_handler import router as moderator_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(register_router)
router.include_router(moderator_router)
router.include_router(echo_router)
