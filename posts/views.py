from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
# Create your views here.

# class based views
@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('add_post')
    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)
    

# update with view
@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id' 
    success_url = reverse_lazy('profile')

# delete with view
@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'delete.html'
    success_url = reverse_lazy('homepage')
    pk_url_kwarg = 'id'



# show details of post
class DetailsView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data = self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments 
        comment_form = forms.CommentForm()
        context['comments']= comments
        context['comment_form']= comment_form
        return context
    








# function based
def add_post(request):
    if request.method == 'POST': # user post request koreche
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('add_post')
    
    else: # user normally website e gele blank form pabe
        post_form = forms.PostForm()
    return render(request, 'add_post.html', {'form' : post_form})

def edit_post(request, id):
    post = models.Post.objects.get(pk=id) 
    post_form = forms.PostForm(instance=post)
    # print(post.title)
    if request.method == 'POST': # user post request koreche
        post_form = forms.PostForm(request.POST, instance=post) # user er post request data ekhane capture korlam
        if post_form.is_valid(): # post kora data gula amra valid kina check kortechi
            post_form.save() # jodi data valid hoy taile database e save korbo
            return redirect('homepage') # sob thik thakle take add author ei url e pathiye dibo
    
    return render(request, 'add_post.html', {'form' : post_form})


def delete_post(request, id):
    post = models.Post.objects.get(pk=id) 
    post.delete()
    return redirect('homepage')