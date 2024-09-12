from django.contrib import admin
from .models import User, Role
from schedule.tasks import send_email, generate_temporary_password


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'role')

    def save_model(self, request, obj, change, form):
        super().save_model(request, obj, change, form)

        if not form and obj.role.title == "Специалист":
            obj.password = generate_temporary_password()
            title = 'Учетные данные для входа на сайт'
            message = f'Добрый день!\nВаш логин: {obj.email}\nВаш временный пароль: {obj.password}'
            sub_list = obj.email
            send_email(title, message, sub_list)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
