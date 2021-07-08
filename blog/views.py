from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm


def list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        model = Post.objects.filter(title__icontains=search_query)
    else:
        model = Post.objects.all()

    paginator = Paginator(model, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    # is_paginated = page.has_other_pages()
    #
    # if page.has_previous():
    #     prev_url = '?page={}'.format(page.previous_page_number())
    # else:
    #     prev_url = ''
    #
    # if page.has_next():
    #     next_url = '?page={}'.format(page.next_page_number())
    # else:
    #     next_url = ''

    # context = {'page_object': page,'is_paginated': is_paginated,'next_url': next_url,'prev_url': prev_url}

    return render(request, 'blog/list.html', {'posts': page})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

    # def get(self, request, slug):
    #     post = get_object_or_404(Post, slug__iexact=slug)
    #     return render(request, 'blog/post_detail.html', {'post': post})


class PostCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create_form.html', {'form': form})

    def post(self, request):
        bound_form = PostForm(request.POST)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/post_create_form.html', {'form': bound_form})


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'list'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'

    # def get(self, request, slug):
    #     tag = get_object_or_404(Tag, slug__iexact=slug)
    #     return render(request, 'blog/tag_detail.html', {'tag': tag})


class TagCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = TagForm()
        return render(request, 'blog/tag_create.html', {'form': form})

    def post(self, request):
        bound_form = TagForm(request.POST)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_create.html', {'form': bound_form})


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True

    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(instance=tag)
    #     return render(request, 'blog/tag_update_form.html', {'form': bound_form, 'tag': tag})
    #
    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(request.POST, instance=tag)
    #
    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         print(new_tag)
    #         return redirect(new_tag)
    #     return render(request, 'blog/tag_update_form.html', {'form': bound_form, 'tag': tag})


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     return render(request, 'blog/tag_delete_form.html', {'tag': tag})
    #
    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     tag.delete()
    #     return redirect(reverse('tags_list_url'))


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', {'tags': tags})
