from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import Post, Category

class PostView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        # Если выбрана категория, отображаем посты по этой категории
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            posts_by_category = Post.objects.filter(category=category).order_by('-date')
        else:
            category = None
            posts_by_category = Post.objects.all().order_by('-date')

        # Посты по категориям (3 поста на категорию)
        category_posts = {
            category: Post.objects.filter(category=category).order_by('-date')[:3]
            for category in categories
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Если это AJAX-запрос, возвращаем только блок постов
            return render(request, 'blog/blog.html', {
                'post_list': posts_by_category,
                'categories': categories,
                'category_posts': category_posts,
                'category': category,
            })
        else:
            # Если это обычный запрос, возвращаем всю страницу
            return render(request, 'blog/blog.html', {
                'post_list': posts_by_category,
                'categories': categories,
                'category_posts': category_posts,
                'category': category,
            })

class PostDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'blog/post_detail.html', {'post': post})
