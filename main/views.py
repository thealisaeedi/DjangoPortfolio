from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, CommentForm
from django.contrib import messages
from .models import Project, Resume, BlogPost, Category, SkillCategory, About
from .models import Education, Experience
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    latest_projects = Project.objects.all().order_by('-id')[:3]
    return render(request, "home.html", {"latest_projects": latest_projects})

def about(request):
    about =  About.objects.first() # only one entry
    return render(request, 'about.html', {'about': about})

def skills(request):
    categories = SkillCategory.objects.prefetch_related('skills').all()
    return render(request, 'skills.html', {'categories': categories})

def projects(request):
    all_projects = Project.objects.all()
    return render(request, "projects.html", {"projects": all_projects})

def resume(request):
    academic_resumes = Resume.objects.filter(category='Academic') # Get the latest resume
    professional_resumes = Resume.objects.filter(category='Professional')
    return render(request, "resume.html", {"academic_resumes": academic_resumes,
                                           "professional_resumes": professional_resumes
                                           })

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Normally you send an email here
            name = form.cleaned_date['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # for now just show success message
            messages.success(request, "Your message has been sent successfully!.")
            form = ContactForm() # reset form
    else: 
        form = ContactForm()
    return render(request, "contact.html", {"form": form})

def experience(request):
    education_list = Education.objects.all()
    experience_list = Experience.objects.all()

    return render(request, 'experience.html', {
        'education_list': education_list,
        'experience_list': experience_list,
    })

def blog_list(request):
    query = request.GET.get("q") # get search term from url
    category_slug = request.GET.get("category")

    posts = BlogPost.objects.all().order_by('-created_at')

    if query: 
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(posts, 6) # posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, "blog/blog_list.html", {
        "page_obj": page_obj,
        "query": query, 
        "categories": categories,
        "selected_category": category_slug, 
        })
 
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.filter(approved=True) # fetch related comments

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.approved = False
            new_comment.save()
            messages.success(request, "Your comment has been submitted awaiting for approval")
            return redirect("blog_detail", pk=post.pk)
    else:
        form = CommentForm()


    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        }) 

def blog_archive(request, year, month): 
    posts = BlogPost.objects.filter(created_at__year=year, created_at__month=month)
