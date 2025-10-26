from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
    path("resume/", views.resume, name="resume"),
    path("experience/", views.experience, name="experience"),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path("archive/<int:year>/<int:month>/", views.blog_archive, name="blog_archive"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    