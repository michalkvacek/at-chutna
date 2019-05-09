from django.contrib import admin

from crawler.models import RestaurantScraperConfig, RecipeIngredientCrawler

class ScrapperConfigAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ('__str__',)


class RecipeCrawlerAdmin(admin.ModelAdmin):
    explode = []
    list_display = ('__str__',)


admin.site.register(RestaurantScraperConfig, ScrapperConfigAdmin)
admin.site.register(RecipeIngredientCrawler, RecipeCrawlerAdmin)
