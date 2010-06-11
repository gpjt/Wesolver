from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('ui/user_page.html', {'user': user})
