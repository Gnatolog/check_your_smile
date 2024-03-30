from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import ResultDiagnostic
from diagnostic.models import Diagnostic


# Create your views here.


def load_result(request, diagnostic_slug=None):
    diagnostic = None
    diagnostics = Diagnostic.objects.all()
    if diagnostic_slug:
        diagnostic = get_object_or_404(Diagnostic,
                                       slug=diagnostic_slug)

    return render(request,
                  'result_template/result_page.html',
                  context={'diagnostic': diagnostic,
                           'diagnostics': diagnostics})


def load_type_result_photo(request):
    all_photo_diagnostics = (
        ResultDiagnostic.objects.filter(user=request.user.id))

    if request.method == 'POST':

        result_diagnostic = ResultDiagnostic.objects.filter(name=request.POST.get('choice'))

        return render(request,
                      'result_template/result_photo.html',
                      context={'result_diagnostic': result_diagnostic}
                      )

    return render(request,
                  'result_template/list_result_type_photo.html',
                  context={'all_photo_diagnostics': all_photo_diagnostics}
                  )

