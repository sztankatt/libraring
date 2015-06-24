from django.shortcuts import render, render_to_response

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from drealtime import iShoutClient
ishout_client = iShoutClient()

# Create your views here.

@login_required
def home(request):
	users = User.objects.exclude(id=request.user.id)

	variables = {'users':users}

	return render(request, 'realtime_test.html', variables)

@login_required
def alert(request):
	r = request.GET.get

	ishout_client.emit(
		int(r('user')),
		'alertchannel',
		data = {'msg':'Hello Dear Friend!'}
		)

	return HttpResponseRedirect(reverse('realtime_test:home'))