from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost


# 1. Список статей (с фильтрацией)
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # ВАЖНО: Возвращаем только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)


# 2. Детальная страница (с увеличением просмотров)
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Получаем объект стандартным способом
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счётчик просмотров
        obj.views += 1
        # Сохраняем ТОЛЬКО поле views (чтобы не перезаписывать всё подряд)
        obj.save(update_fields=['views'])
        return obj


# 3. Создание статьи
class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    # Поля, которые пользователь может заполнить
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog_list')


# 4. Редактирование статьи (с редиректом на саму статью)
class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']

    def get_success_url(self):
        # ВАЖНО: Перенаправляем на страницу этой же статьи после редактирования
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.pk})


# 5. Удаление статьи
class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog_list')
