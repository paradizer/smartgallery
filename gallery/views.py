# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Images, User
from .forms import ImageForm


class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"
    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


@login_required
def home(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            newimg = Images(imgfile=request.FILES['docfile'])
            newimg.user = request.user
            newimg.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ImageForm()  # A empty, unbound form
    # Load documents for the list page
    images = Images.objects.all()
    # Render list page with the documents and the form
    return render(
        request,
        'gallery/index.html',
        {'images': images, 'form': form}
    )

@login_required
def profile(request):
    profile = User.objects.get(id=request.user.id)
    # Handle file upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            newimg = Images(imgfile=request.FILES['docfile'])
            newimg.user = request.user
            newimg.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ImageForm()  # A empty, unbound form
    # Render list page with the documents and the form
    images = Images.objects.filter(user=request.user.id)
    return render(
        request,
        'gallery/profile.html',
        {'profile': profile, 'images': images, 'form': form}
    )
