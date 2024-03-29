from django.contrib import admin
from .models import Post,Category,Profile


# Register your models here.

#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','publish','status']
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status','publish')



admin.site.register(Category)
admin.site.register(Profile)

