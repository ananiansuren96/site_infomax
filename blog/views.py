from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import Post, Category
from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
                Disallow: /admin/
                Disallow: /private/
                Disallow: /admin/
                Disallow: /profile/
                Disallow: /cart/
                Disallow: /orders/
                Disallow: /filter/
                Disallow: /private/
                Disallow: /tmp/
                Disallow: /debug/
                Disallow: /api/
                Sitemap: https://infomax.space/sitemap.xml
                """
    return HttpResponse(content, content_type="text/plain")

class PostView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        category_1 = get_object_or_404(Category, id=6)
        post_list_category_1 = Post.objects.filter(category=category_1).order_by('-date')[:1]

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
        popular_posts = Post.objects.order_by('-views_count')[:6]

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Если это AJAX-запрос, возвращаем только блок постов
            return render(request, 'blog/blog.html', {
                'post_list_category_1': post_list_category_1,
                'post_list': posts_by_category,
                'categories': categories,
                'category_posts': category_posts,
                'category': category,
                'popular_posts': popular_posts,
            })
        else:
            # Если это обычный запрос, возвращаем всю страницу
            return render(request, 'blog/blog.html', {
                'post_list_category_1': post_list_category_1,
                'post_list': posts_by_category,
                'categories': categories,
                'category_posts': category_posts,
                'category': category,
                'popular_posts': popular_posts,
            })

class PostDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.views_count += 1
        post.save(update_fields=['views_count'])  # Исправлено "update_fields"        
        popular_posts = Post.objects.order_by('-views_count')[:6]

        return render(request, 'blog/post_detail.html', {
            'post': post,
            'popular_posts': popular_posts,
        })