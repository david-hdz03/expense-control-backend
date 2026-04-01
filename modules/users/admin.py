from sqladmin import ModelView

from .models import User, UserType


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_active]
    column_searchable_list = [User.email]
    icon = "fa-solid fa-user"


class UserTypeAdmin(ModelView, model=UserType):
    column_list = [UserType.id, UserType.name]
    icon = "fa-solid fa-tags"
