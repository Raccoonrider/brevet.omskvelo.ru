from django.utils import timezone
from django.contrib import admin
from django.contrib import messages

from inventory.models import Medal, Price

class DistanceFilter(admin.SimpleListFilter):
    title = "Дистанция"
    parameter_name = 'event_distance'

    def lookups(self, request, model_admin):
        return (
            ("200", "200"), 
            ("300", "300"), 
            ("400", "400"), 
            ("600", "600"), 
            ("1000", "1000"), 
            ("1200+", "1200+"), 
        )

    def queryset(self, request, queryset):
        if self.value() == "1200+":
            queryset = queryset.filter(event__route__lrm=True)
        elif self.value():
            queryset = queryset.filter(event__route__distance=self.value())
        return queryset.all()


class YearFilter(admin.SimpleListFilter):
    title = "Год"
    parameter_name = 'event_year'

    def lookups(self, request, model_admin):
        qs = Medal.objects.order_by('-event__date__year').distinct('event__date__year')
        return tuple((x.event.date.year, x.event.date.year) for x in qs)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(event__date__year=self.value())
        return queryset.all()



@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    autocomplete_fields = ('randonneur',)
    search_fields = ('randonneur__russian_surname',)
    list_display = ('__str__', 'get_event_date', 'payment', 'is_ordered', 'is_received', 'is_removed',)
    list_filter = ('payment', DistanceFilter, YearFilter)
    sortable_by = ('__str__', 'get_event_date', 'payment', 'is_ordered', 'is_received', 'is_removed',)
    actions = ('action_order', 'action_receive', 'action_payment', 'action_remove')

    @admin.display(description="Заказана", boolean=True)
    def is_ordered(self, instance:Medal):
        return instance.ordered is not None

    @admin.display(description="В наличии", boolean=True)
    def is_received(self, instance:Medal):
        return instance.received is not None
    
    @admin.display(description="Вручена", boolean=True)
    def is_removed(self, instance:Medal):
        return instance.removed is not None
    
    @admin.display(description="Дата")
    def get_event_date(self, instance:Medal):
        return instance.event.date
    
    def generic_action(self, request, queryset, action:callable, success_text, error_text):
        fails = []
        for item in queryset:
            try:
                action(item)
            except:
                fails.append(str(item))

        if fails:
            self.message_user(
                request,
                f"{error_text}: {', '.join(fails)}",
                messages.ERROR,
            )
        else:
            self.message_user(
                request,
                f"{success_text}: {len(queryset)}",
                messages.SUCCESS,
            )
    
    @admin.action(description="Отметить заказ")
    def action_order(self, request, queryset):
        def action(item:Medal):
            if item.ordered is None:
                item.ordered = timezone.now()
                item.save()

        return self.generic_action(
            request, queryset, action,
            success_text="Успешно заказаны",
            error_text="Ошибка"
        )


    @admin.action(description="Отметить приём")
    def action_receive(self, request, queryset):
        def action(item:Medal):
            if item.received is None:
                item.received = timezone.now()
                item.save()

        return self.generic_action(
            request, queryset, action,
            success_text="Успешно приняты",
            error_text="Ошибка"
        )
    

    @admin.action(description="Отметить оплату")
    def action_payment(self, request, queryset):
        def action(item:Medal):
            if not item.payment:
                item.payment = True
                item.save()

        return self.generic_action(
            request, queryset, action,
            success_text="Успешно заказаны",
            error_text="Ошибка"
        )
    

    @admin.action(description="Отметить вручение")
    def action_remove(self, request, queryset):
        def action(item:Medal):
            if item.removed is None:
                item.removed = timezone.now()
                item.save()

        return self.generic_action(
            request, queryset, action,
            success_text="Успешно вручены",
            error_text="Ошибка"
        )
    

admin.site.register(Price)