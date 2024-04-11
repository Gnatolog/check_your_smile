from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Diagnostic, PhotoDiagnostic
from .forms import PhotoDiagnosticForm, ResultDiagnosticForm
from result.models import ResultDiagnostic
import requests
import asyncio
import aiohttp


# Create your views here.


def load_diagn(request, diagnostic_slug=None):
    diagnostic = None
    diagnostics = Diagnostic.objects.all()
    if diagnostic_slug:
        diagnostic = get_object_or_404(Diagnostic,
                                       slug=diagnostic_slug)

    return render(request,
                  'diagnostic_template/diagnostic_page.html',
                  context={'diagnostic': diagnostic,
                           'diagnostics': diagnostics})









def get_module_analiz(name, path,
                      name_file_lateral,
                      name_file_frontal):
    r = requests.get('http://127.0.0.1:8000/data_analiz/' + name + '/' +
                     path + '/' + name_file_lateral + '/' + name_file_frontal)

    if r.status_code == 200:
        return r.json()


def photo_diagnostic(request):
    if request.method == 'POST':

        form = PhotoDiagnosticForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            path = ''
            name_file_lateral = ''
            name_file_frontal = ''
            for item in PhotoDiagnostic.objects.filter(name=request.POST.get('name')):
                path = str(item.image_lateral).split('/')[1]
                name_file_lateral = str(item.image_lateral).split('/')[3]
                name_file_frontal = str(item.image_frontal).split('/')[3]

        img_obj = form.instance
        result_diagnostic = get_module_analiz(str(request.user),
                                              path=path,
                                              name_file_lateral=name_file_lateral,
                                              name_file_frontal=name_file_frontal
                                              )
        result = ResultDiagnostic
        result.objects.create(
            name=request.POST.get('name'),
            user=request.user,
            result_diagnostic=result_diagnostic,
            type_diagnostic='photo')

        return render(request, 'diagnostic_template/photo_diagnostic.html',
                      context={'form': form,
                               'img_obj': img_obj}
                      )
    else:
        form = PhotoDiagnosticForm()
    return render(request, 'diagnostic_template/photo_diagnostic.html',
                  {'form': form})
