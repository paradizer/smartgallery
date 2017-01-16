from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

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

#@login_required
def home(request):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(vars(request))
    template = loader.get_template('gallery/index.html')
    context = RequestContext(request, { "user": request.user
    })
    pp.pprint(vars(HttpResponse(template.render(context))))
    return HttpResponse(template.render(context))
