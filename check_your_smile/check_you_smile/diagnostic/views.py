from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Diagnostic, PhotoDiagnostic
from .forms import PhotoDiagnosticForm
from result.models import ResultDiagnostic
from .tasks import get_module_analiz



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

            results = get_module_analiz.delay(name=str(request.user),
                                              path=path,
                                              name_file_lateral=name_file_lateral,
                                              name_file_frontal=name_file_frontal)

            result = ResultDiagnostic
            result.objects.create(
                name=request.POST.get('name'),
                user=request.user,
                result_diagnostic=str(results),
                type_diagnostic='photo')

        return render(request, 'diagnostic_template/photo_diagnostic_start.html', )

    else:
        form = PhotoDiagnosticForm()
    return render(request, 'diagnostic_template/photo_diagnostic.html',
                  {'form': form})
