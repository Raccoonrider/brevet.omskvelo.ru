from django.contrib import admin
from django.http import HttpResponseRedirect

from users.models import User
from users.forms import SignUpForm

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    add_form = SignUpForm
    autocomplete_fields = ('randonneur',)
    search_fields = ('first_name', 'last_name')
    change_form_template = 'admin/change_user.html'
    list_display = ('get_display_name','phone_number','oauth',)
    exclude = ('groups','user_permissions', 'is_staff')
    ordering = ('last_name', 'first_name')

    def response_change(self, request, obj):
        if "_generate-randonneur" in request.POST:

            if (obj.create_randonneur()):
                obj.save()
                self.message_user(request, "Рандоннёр сгенерирован успешно!")
                return super().response_change(request, obj)
            else:
                self.message_user(request, "Невозможно сгенерировать рандоннёра. К учетной записи уже привязан рандоннёр.", level="ERROR")
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)
