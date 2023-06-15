from django.contrib import admin
from .models import BlogPost, Comment, BlogUser, Block


class BlogUserAdmin(admin.ModelAdmin):
    list_display = ("user", "name")

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.user_id == request.user.id or request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user_id == request.user.id or request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False



class BlogPostAdmin(admin.ModelAdmin):

    list_display = ("title", "user")
    search_fields = ["title", "content"]
    list_filter = ["creation_date"]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.user_id == request.user.id or request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None and (obj.user_id == request.user.id or obj.post.user_id == request.user.id) or request.user.is_superuser:
            return True
        return False

    def has_module_permission(self, request):
        return True


class BlockAdmin(admin.ModelAdmin):

    exclude = ('blocker', )

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        obj.blocker = BlogUser.objects.get(user=request.user)
        super(BlockAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "blocked":
            kwargs["queryset"] = BlogUser.objects.exclude(user=request.user)
            kwargs["queryset"] = BlogUser.objects.exclude(user__username='admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Block, BlockAdmin)