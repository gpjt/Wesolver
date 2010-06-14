from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404

from wesolver.spreadsheet.models import Spreadsheet


@login_required
def user_page(request, username):
    user = get_object_or_404(User, username=username)
    sheets = Spreadsheet.objects.filter(owner=user)
    return render_to_response('ui/user_page.html', { 'user' : user, 'sheets' : sheets, 'my_page' : (user == request.user)})


def get_user_sheet(username, sheet_id):
    user = get_object_or_404(User, username=username)
    sheet = get_object_or_404(Spreadsheet, pk=sheet_id)
    if sheet.owner != user:
        raise Http404
    return user, sheet


class CreateSheetForm(ModelForm):
    class Meta:
        model = Spreadsheet
        fields = (
            'name',
        )

@login_required
def create_sheet(request, username):
    if request.method == "POST":
        form = CreateSheetForm(request.POST)

        if form.is_valid():
            sheet = form.save(commit=False)
            sheet.owner = request.user
            sheet.save()
            return HttpResponseRedirect(reverse('show-user', args=[request.user]))


    else:
        form = CreateSheetForm()

    return render_to_response("ui/create_sheet.html", { "form" : form } )


@login_required
def sheet_page(request, username, sheet_id):
    user, sheet = get_user_sheet(username, sheet_id)
    return render_to_response('ui/sheet_page.html', { 'user' : user, 'sheet' : sheet })

@login_required
def sheet_json(request, username, sheet_id):
    _, sheet = get_user_sheet(username, sheet_id)
    return HttpResponse(sheet.json())


@login_required
def sheet_update(request, username, sheet_id):
    _, sheet = get_user_sheet(username, sheet_id)
    value = request.GET["value"]
    section = request.GET.get("section")
    if section:
        sheet.update_user_code(section, value)
    else:
        col = int(request.GET["col"])
        row = int(request.GET["row"])
        sheet.update((col, row), value)
    sheet.save()
    return HttpResponse("")
