from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.admin.options import csrf_protect_m


from .models import News, Image, EntryPoint, SendNews, AsqQuestion, AboutProjectButton, Contact, JustSend, User, AboutProjectContent
# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    max_num=1
    fields = ['image_path']
    readonly_fields = ('image_path',)
    verbose_name = 'Изображения'
    verbose_name_plural = 'Изображения'

    def image_path(self, image: Image):
        img = f'/{image.path}'
        from django.utils.html import format_html
        return format_html('<img src = "%s" width = "350" style="object-fit:cover">'% (img))


class NewsAdmin(admin.ModelAdmin):
    fields = ['user_url','content', 'send_date']
    readonly_fields = ('user_url','content','send_date')
    inlines = [ImageInline]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def user_url(self, news:News):
        url = f'https://t.me/{news.user_name}'
        from django.utils.html import format_html

        return format_html("<a href='%s'>%s</a>" % (url, url))

    user_url.short_description = 'Ссылка на пользователя'


class AboutProjectButtonAdmin(admin.ModelAdmin):
    fields = ['button_name', 'url']
    list_display = ['button_name']


class SingletonModelAdmin(admin.ModelAdmin):
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        instance = self.model.objects.first()
        return self.changeform_view(
                request=request,
                object_id=str(instance.id) if instance else None,
                extra_context=extra_context)

    def has_add_permission(self, request):
        return not self.model.objects.exists()


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ('user_url', 'chat_id','first_name', 'last_name', 'date_joined')
    list_display = ('username', 'user_id', 'first_name', 'last_name', 'date_joined')
    form = MyUserChangeForm
    fieldsets = (
        (None, {"fields": ("user_url" ,"password")}),) + (
        (None, {'fields': ('chat_id','first_name', 'last_name', 'date_joined')}),
    )
    exclude = ('email',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def user_url(self, user:User):
        url = f'https://t.me/{user.username}'
        from django.utils.html import format_html

        return format_html("<a href='%s'>%s</a>" % (url, url))

    user_url.short_description = 'Ссылка на пользователя'


admin.site.register(News,NewsAdmin)
admin.site.register(EntryPoint,SingletonModelAdmin)
admin.site.register(SendNews,SingletonModelAdmin)
admin.site.register(AsqQuestion,SingletonModelAdmin)
admin.site.register(AboutProjectButton,AboutProjectButtonAdmin)
admin.site.register(AboutProjectContent,SingletonModelAdmin)
admin.site.register(Contact,SingletonModelAdmin)
admin.site.register(JustSend,SingletonModelAdmin)
admin.site.register(User,CustomUserAdmin)
admin.site.unregister(Group)
