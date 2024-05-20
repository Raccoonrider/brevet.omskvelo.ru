import re

from django.contrib import admin
from django.http import HttpResponseRedirect

from brevet_database.models import Club, Randonneur, Result, Event, Route, Application, PaymentInfo
from brevet_database.forms import AdminResultForm

result_pattern = re.compile("^\d\d\:\d\d$")

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    model = Result
    form = AdminResultForm
    autocomplete_fields = ('randonneur',)
    list_display = ('get_route', 'get_date', 'randonneur', 'get_time', 'homologation', 'medal')

    @admin.display(description='Маршрут')
    def get_route(self, instance:Result):
        return str(instance.event.route)
    
    @admin.display(description='Время')
    def get_time(self, instance:Result):
        return str(instance.get_time())
    
    @admin.display(description='Дата')
    def get_date(self, instance:Result):
        return str(instance.get_date())


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        default_event = Event.objects.filter(finished=False).order_by("date").first()
        if default_event:
            form.base_fields['event'].initial = default_event
        return form        

@admin.register(Randonneur)
class RandonneurAdmin(admin.ModelAdmin):
    search_fields = ('russian_surname', 'russian_name')
    readonly_fields = ('sr', 'total_distance', 'total_brevets')
    change_form_template = 'admin/change_randonneur.html'
    list_display = ('__str__', 'translit')
    list_filter = ('female', 'club',)
    ordering = ('surname', 'name')

    def response_change(self, request, obj):
        if "_update_stats" in request.POST:
            if (obj.update_stats()):
                self.message_user(request, "Статистика успешно обновлена")
                return super().response_change(request, obj)
            else:
                self.message_user(request, "Что-то пошло не так", level="ERROR")
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    raw_id_fields = ['result']
    autocomplete_fields = ['user', 'event']
    search_fields = ('user__last_name', 'event__route__name')
    list_display = ('user__name', 'event', 'active')
    list_filter = ('active', 'dnf', 'dns', 'dsq', 'otl', 'payment')

    @admin.display(description='Пользователь')
    def user__name(self, instance:Application):
        return f"{instance.user.last_name} {instance.user.first_name}"

class DistanceAdminFilter(admin.SimpleListFilter):
    title = 'Дистанция'
    parameter_name = 'distance'

    def lookups(self, request, model_admin):
        return [
            ('200', '200'),
            ('300', '300'),
            ('400', '400'),
            ('600', '600'),
            ('1000','1000'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            if queryset.model is Route:
                return queryset.filter(distance=int(self.value()))
            if queryset.model is Event:
                return queryset.filter(route__distance=int(self.value()))

        return queryset

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = ('route__name',)
    list_display = ('route__name', 'distance', 'date', 'finished',)
    list_filter = (DistanceAdminFilter,)
    ordering = ('-date',)

    @admin.display(description='Дистанция')
    def distance(self, instance:Event):
        return instance.route.distance
    
    @admin.display(description='Маршрут')
    def route__name(self, instance:Event):
        return instance.route.name

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    # model = Route
    search_fields = ('name','distance')
    list_display = ('name', 'distance')
    list_filter = (DistanceAdminFilter, 'brm', 'lrm', 'fleche', 'sr600')


admin.site.register(Club)
admin.site.register(PaymentInfo)