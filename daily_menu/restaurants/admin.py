from django.contrib import admin

from restaurants.models import Restaurant, DailyMenu


class RestaurantAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ('__str__', 'menu_url')
    search_fields = ('name',)
    list_filter = ('name',)


class DailyMenuAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ('__str__', 'get_restaurant', 'day')
    search_fields = ('name',)
    list_filter = ('day',)

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_restaurant.admin_order_field = 'restaurant'
    get_restaurant.short_description = 'Restaurant Name'


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(DailyMenu, DailyMenuAdmin)
