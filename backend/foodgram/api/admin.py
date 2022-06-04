from api import models
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


class AmountIngredientInLine(admin.TabularInline):
    model = models.RecipeIngredient
    fields = ('ingredient', 'measurement_unit', 'amount')
    readonly_fields = ('measurement_unit', )
    extra = 0

    def measurement_unit(self, obj):
        return obj.ingredient.measurement_unit
    measurement_unit.short_description = 'measurement unit'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    inlines = (AmountIngredientInLine, )

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(models.Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(models.Favorite)
admin.site.register(models.Cart)
