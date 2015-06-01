# -*- coding: utf-8 -*-
from hashlib import md5
from django.core.mail import send_mail
from django.db import transaction
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.shortcuts import render, HttpResponse


from forms import RegistrationForm
from accounts.models import RegConfirm

def index(request):
    return render(request, 'accounts/frontend/index.html')


#def login(request):
#    if request
#    return render(request, 'frontend/login.html')

def logout(request):
    pass

def register(request):
    pass


@transaction.atomic
def registration(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=False,
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            hash = md5(str(user.id) + form.cleaned_data['username']).hexdigest()
            confirm = RegConfirm(hash=hash, user_id=user.id)
            confirm.save()
            current_site = Site.objects.get(id=1)
            message = u'Поздравляем! Вы зарегистрировались на %s . Пожалуйста, пройдите по адресу %s для активации учетной записи.' % \
                      (current_site.domain, "http://" + current_site.domain + "/accounts/confirm/" + hash, )


            send_mail(u'Активация аккаунта ' + current_site.domain, message, 'system@'+current_site.domain,
                [form.cleaned_data['email']])

            return render(request, 'accounts/frontend/registration_done.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/frontend/registration.html', {
        'form':form
    })
@transaction.atomic
def confirm_registration(request, hash):
    try:
        confirm = RegConfirm.objects.get(hash=hash)
    except RegConfirm.DoesNotExist:
        return HttpResponse(u'Код подтверждения не верен')
    try:
        user = User.objects.get(id=confirm.user_id)
    except User.DoesNotExist:
        return HttpResponse(u'Код подтверждения не верен')

    if user.is_active == False:
        #тут надо создать пользователя в лдапе
        user.is_active = True
        group = Group.objects.get(name='users')
        user.groups.add(group)
        user.save()
        confirm.delete()
    return render(request,  'accounts/frontend/registration_confirm.html')

