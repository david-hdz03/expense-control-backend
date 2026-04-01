from sqladmin import Admin

from modules.users.admin import UserAdmin, UserTypeAdmin

# Cuando agregues admins en otros módulos, impórtalos aquí:
# from modules.categories.admin import CategoryAdmin

admin_views = [
    UserAdmin,
    UserTypeAdmin,
]


def setup_admin(admin: Admin) -> None:
    for view in admin_views:
        admin.add_view(view)
