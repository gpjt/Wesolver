from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404

from wesolver.spreadsheet.models import Spreadsheet


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    sheets = Spreadsheet.objects.filter(owner=user)
    return render_to_response('ui/user_page.html', { 'user' : user, 'sheets' : sheets})



def get_user_sheet(username, sheet_id):
    user = get_object_or_404(User, username=username)
    sheet = get_object_or_404(Spreadsheet, pk=sheet_id)
    if sheet.owner != user:
        raise Http404
    return user, sheet
    

def sheet_page(request, username, sheet_id):
    user, sheet = get_user_sheet(username, sheet_id)
    return render_to_response('ui/sheet_page.html', { 'user' : user, 'sheet' : sheet})
    
    
def sheet_json(request, username, sheet_id):
    _, sheet = get_user_sheet(username, sheet_id)
    return render_to_response('ui/sheet_json.html', { 'sheet' : sheet})