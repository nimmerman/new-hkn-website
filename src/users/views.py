from django.shortcuts import render

# Create your views here.
from .models import Member
from .models import Electee
from .models import Social
from .models import Service_Hours
from .forms import MemberForm
from .forms import SocialForm
from .forms import ServiceHoursForm
from .status import is_officer
from .status import is_electee
from hknWebsiteProject.resume_zip import zip_resumes
import string

def member_list(request):
	member_list = Member.objects.all().filter(first_name__isnull=False).filter(last_name__isnull=False)
	member_list = member_list.exclude(first_name__exact="").exclude(last_name__exact="")
	member_list = member_list.order_by('first_name','last_name')

	context = {
		'member_list' : member_list
	}

	return render(request, "member_list.html", context)


def profile(request, uniqname):
	if request.user.is_anonymous():
		context = {
			'error' : True,
			'error_msg' : 'You must be a member to see member\'s profiles'
		}
	else:
		is_curr_user = (request.user.username == uniqname)

		m = Member.objects.get(uniqname = uniqname)

		electee_progress = is_electee(uniqname) and (uniqname == request.user.username or is_officer(request.user.username))
		
		context = {
			'profile': m,
			'is_curr_user': is_curr_user,
			'electee_progress' : electee_progress,
			'error' : False,
		}

	return render(request, "profile.html", context)

def profile_edit(request, uniqname):
	context = {}
	if request.user.is_anonymous() or uniqname != request.user.username:
		context = {
			'error' : True,
			'error_msg' : 'You cannot edit this profile'
		}
	else:
		context['profile_saved'] = False
		m = Member.objects.get(uniqname = uniqname)
		form = MemberForm(instance = m)	

		if request.POST:
			form = MemberForm(request.POST, request.FILES, instance = m)
			if form.is_valid():
				form.save()
				zip_resumes()
				context['profile_saved'] = True
				context['profile'] = m
				context['is_curr_user'] = 'is_curr_user'

				return render(request, "profile.html", context)

		context['form'] = form

	return render(request, "profile_edit.html", context)

def electee_progress(request, uniqname):
	if request.user.is_anonymous() or (uniqname != request.user.username and not is_officer(request.user.username)):
		context = {
			'error' : True,
			'error_msg' : 'You cannot see this electee\'s progress'
		}
	else:
		e = Electee.objects.get(member_id = uniqname)

		context = {
			'error' : False,
			'e' : e,
			'submit' : False,
		}

		if (uniqname == request.user.username):
			context['submit'] = True

	return render(request, "electee_progress.html", context)

def all_electees(request):
	electee_list = Electee.objects.filter(member__status='E')

	context = {
		'electee_list' : electee_list
	}

	return render(request, "all_electees.html", context)

def submit_social(request):
	print '------------submit_social-------------'
	if request.user.is_anonymous() or not is_electee(request.user.username):
		context = {
			'error' : True,
			'error_msg' : 'You must be an electee to submit socials'
		}
	else:
		context = {
			'error' : False,
			'social_submitted' : False
		}

		form = SocialForm(request.POST or None)
		if request.POST:
			if form.is_valid():
				social = form.save(commit=False)
				social.electee = Electee.objects.get(member_id = request.user.username)
				social.save()
				form = SocialForm(None)
				context['social_submitted'] = True

		context['form'] = form

	return render(request, "submit_social.html", context)

def submit_service_hours(request):
	if request.user.is_anonymous() or not is_electee(request.user.username):
		context = {
			'error' : True,
			'error_msg' : 'You must be an electee to submit service hours'
		}
	else:
		context = {
			'error' : False,
			'service_hours_submitted' : False
		}

		form = ServiceHoursForm(request.POST or None)
		if request.POST:
			if form.is_valid():
				social = form.save(commit=False)
				social.electee = Electee.objects.get(member_id = request.user.username)
				social.save()
				form = ServiceHoursForm(None)
				context['service_hours_submitted'] = True

		context['form'] = form

	return render(request, "submit_service_hours.html", context)

def electee_submission_approval(request):
	social_list = Social.objects.filter(approved='0')
	service_hour_list = Service_Hours.objects.filter(approved='0')

	context = {
		'social_list' : social_list,
		'service_hour_list' : service_hour_list,
	}

	return render(request, "electee_submission_approval.html", context)
