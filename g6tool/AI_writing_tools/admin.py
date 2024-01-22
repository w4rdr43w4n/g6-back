from django.contrib import admin
from .models import WikiRewrittenSectionsModel ,ArticlesModel,ImprovementModel,CompletionModel


class WikiModelAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in WikiRewrittenSectionsModel._meta.get_fields()]



admin.site.register(WikiRewrittenSectionsModel, WikiModelAdmin)
admin.site.register(ArticlesModel)
admin.site.register(ImprovementModel)
admin.site.register(CompletionModel)
