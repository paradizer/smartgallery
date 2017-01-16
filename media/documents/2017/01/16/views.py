from django.shortcuts import render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _

import hashlib
import random
import string

from trengine.main import create_account

from authentication.models import User
from .forms import QuickSignUpForm,SignInForm,CaptchaSignUpForm,SignUpForm
from user.models import UserProfile
from referral_system.models import Referrer,create_ref_tree
from core.core import get_sitesettings

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		return redirect('user:profile',request.user.id)
	else:
		return redirect('authentication:signin')

def signup(request):
	site_settings=get_sitesettings()
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data.get('username')
			email=form.cleaned_data.get('email')
			password=form.cleaned_data.get('password')
			User.objects.create_user(username=username,email=email,password=password)
			user=authenticate(username=username,password=password)
			user_profile=get_object_or_404(UserProfile,pk=user)
			
			try:
				ref_url=request.session['ref_url']	
				referrer_id=UserProfile.objects.get(ref_url=ref_url).user.id
				referrers=create_ref_tree(referrer_id)
				Referrer.objects.create(user=user,referrer_id=referrer_id,referrers=referrers)
			except:
				pass

			login(request,user)
			messages.success(request,_("Confirmation link has been sent to {0}").format(email))

			return redirect('user:profile',user.id)
		else:
			messages.add_message(request,messages.ERROR,_('There is some problems with creating your account.'))
			return render(request,'chain/signup.html',{'form': form,'site_settings':site_settings})
	else:
		return render(request,'chain/signup.html',{'form': SignUpForm(),'site_settings':site_settings})

def quick_signup(request):
	if request.method=='POST':
		form=QuickSignUpForm(request.POST)
		if form.is_valid():
			length=10
			username=get_unique_username(length)
			password=get_random_password(length)
			email=form.cleaned_data.get('email')
			try:
				send_mail(
						'MLMengine registration',
						'Username: {0}, Password: {1}'.format(username,password),
						settings.EMAIL_HOST_USER,
						[email],
					)
			except:
				messages.error(request,'Invalid email')
				return render(request,'chain/quick_signup.html',{'form': form,'site_settings':site_settings})
				
			User.objects.create_user(username=username,email=email,password=password)

			messages.success(request,'Password: {}'.format(password))

			user=authenticate(username=username,password=password)		
			user_profile=get_object_or_404(UserProfile,pk=user)
			
			try:
				ref_url=request.session['ref_url']	
				referrer_id=UserProfile.objects.get(ref_url=ref_url).user.id
				referrers=create_ref_tree(referrer_id)
				Referrer.objects.create(user=user,referrer_id=referrer_id,referrers=referrers)
			except:
				pass

			login(request,user)

			return HttpResponseRedirect(reverse('user:profile',args=[user.id]))
		else:
			messages.add_message(request,messages.ERROR,_('Correct inputs below'))
			return render(request,'chain/quick_signup.html',{'form': form,'site_settings':site_settings})
	else:
		site_settings=get_sitesettings()
		return render(request,'chain/quick_signup.html',{'form': QuickSignUpForm(),'site_settings':site_settings})


def quick_signup_captcha(request):
	site_settings=get_sitesettings()
	if request.method=='POST':
			length=10
			username=get_unique_username(length)
			password=get_random_password(length)
				
			User.objects.create_user(username=username,password=password)

			message=_(
					'<strong>Username: </strong>{0}' \
					'<br>' \
					'<strong>Password: </strong>{1}').format(username,password)
			messages.success(request,message)

			user=authenticate(username=username,password=password)		
			user_profile=get_object_or_404(UserProfile,pk=user)
			
			try:
				ref_url=request.session['ref_url']	
				referrer_id=UserProfile.objects.get(ref_url=ref_url).user.id
				referrers=create_ref_tree(referrer_id)
				Referrer.objects.create(user=user,referrer_id=referrer_id,referrers=referrers)
			except:
				pass

			login(request,user)

			return HttpResponseRedirect(reverse('user:profile',args=[user.id]))
	else:
		return render(request,'chain/quick_signup_captcha.html',{'form': QuickSignUpForm(),'site_settings':site_settings})


def get_random_username(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

def get_unique_username(length):
	username=get_random_username(length)
	while(User.objects.filter(username=username).exists()):
		username=get_random_username(length)
	return username

def get_random_password(length):
	return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(length))


def signin(request):
	site_settings=get_sitesettings()
	if request.method=='POST':
		form=SignInForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate(username=username,password=password)	
			if user is not None:	
				login(request,user)
				return HttpResponseRedirect(reverse('user:profile',args=[user.id]))
			else:
				messages.add_message(request,messages.ERROR,_('Username or password is invalid.'))
				return render(request,'chain/signin.html',{'form':form,'site_settings':site_settings})
		else:
			return render(request,'chain/signin.html',{'form':form,'site_settings':site_settings})
	else:
		return render(request,'chain/signin.html',{'form': SignInForm(),'site_settings':site_settings})

def signout(request):
	logout(request)
	return redirect('authentication:signin')

def forgot_password(request):
	site_settings=get_sitesettings()
	if request.method=='POST':
		email=request.POST['email']
		if User.objects.filter(email=email).exists():
			#!!!DEBUG!!!
			user=User.objects.filter(email=email)[0]
			print(user.username)
			new_password=get_random_password(10)

			try:
				message='Your new password: {}'.format(new_password)
				#user.email_user('Forgot password',message)
				send_mail(
						'Forgot password',
						message,
						settings.EMAIL_HOST_USER,
						[email],
					)
			except Exception as e:
				print(e)
				messages.error(request,_('Unable to send a message to your email. Please, try later'))
				return redirect('authentication:forgot_password')

			user.set_password(new_password)
			user.save()
			messages.success(request,_('New password have been sent to your email'))
			return redirect('authentication:signin')
		else:
			messages.error(request,_('User with this email does not exists'))
			return redirect('authentication:forgot_password')
	else:
		return render(request,'chain/forgot-password.html',{'site_settings':site_settings})




