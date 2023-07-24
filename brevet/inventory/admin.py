from django.contrib import admin

from inventory.models import Medal, Price

@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    autocomplete_fields = ('randonneur',)
    search_fields = ('randonneur__russian_surname',)
    list_display = ('__str__', 'get_event_date', 'payment', 'is_ordered', 'is_received', 'is_removed',)
    list_filter = ('payment',)
    sortable_by = ('__str__', 'get_event_date', 'payment', 'is_ordered', 'is_received', 'is_removed',)

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
    
admin.site.register(Price)