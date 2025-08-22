from models import User
from cruds.base import CRUDRepository
from log import get_logger

log = get_logger(__name__)

class UserCRUD(CRUDRepository):
    def __init__(self) -> None:
        super().__init__(User)

user_crud = UserCRUD()
