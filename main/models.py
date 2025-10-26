from django.db import models
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True) # optional Github/ demo link
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Resume(models.Model):

    CATEGORY_CHOICES = [
        ('Academic', 'Academic'),
        ('Professional', 'Professional'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Professional')
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 ,unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True) # New Field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
    
class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )

    def children(self):
        """ Return replies to this comment. """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """ Check if this comment is a top-level comment."""
        return self.parent is None

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
    
class SkillCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon_class =  models.CharField(max_length=50, blank=True, help_text="Optional icon for category")

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    icon_class = models.CharField(max_length=50, help_text="Font Awesome class, e.g. 'fa-brands fa-python'")
    color_class = models.CharField(max_length=20, default="bg-primary", help_text="Bootstrap color class for badge")

    def __str__(self):
        return self.name
    
class About(models.Model):
    title = models.CharField(max_length=100, default="About Me")
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    descripton = models.TextField(blank=True)

    class Meta:
        ordering = ['-end_year']
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
class Experience(models.Model):
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)   
    descriptoin = models.TextField(blank=True)

    class Meta:
        ordering = ['-end_year']
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} at {self.company}"
