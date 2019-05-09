from django.contrib import admin

from crawler.models import Ingredient, Recipe, RecipeCategory


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class RecipeCategoriesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_significant')
    search_fields = ('name','is_significant',)
    list_filter = ('is_significant',)

class IngredientsAdmin(admin.ModelAdmin):
    list_per_page = 10
    exclude = []
    list_display = ('__str__', 'is_significant')
    search_fields = ('name','is_significant',)
    list_filter = ('is_significant',)

admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(RecipeCategory, RecipeCategoriesAdmin)
