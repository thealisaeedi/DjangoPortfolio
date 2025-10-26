from django.contrib import admin
from .models import Project, Resume, BlogPost, Comment, Category, Tag, SkillCategory, Skill, About
from .models import Education, Experience

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {"slug": ("title", )}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_class', 'color_class')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_year', 'end_year')

admin.site.register(Project)
admin.site.register(Resume)
