from django.shortcuts import render

from manager.forms import BrainstormForm


def brainstorm(request):
    template = 'before_login/manager/brainstorm.html'
    if request.POST:
        bf = BrainstormForm(request.POST)
        if bf.is_valid():
            bf.save()
            return render(
                request,
                template, {'success': True})
        else:
            return render(
                request,
                template, {'form': bf, 'success': False})
    else:
        bf = BrainstormForm()
        return render(
            request,
            template, {'form': bf, 'success': False})
