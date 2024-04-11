from django.shortcuts import render, get_object_or_404
from .models import ResultDiagnostic
from diagnostic.models import Diagnostic
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


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

        email = EmailMessage(to=(request.user.email,))

        result_diagnostic = (
            ResultDiagnostic.objects.filter(name=request.POST.get('choice')).filter(user=request.user.id))

        date_diagnostic = ''
        user_name = ''
        lateral_sagital = ''
        lateral_vert = ''
        frontal_hor = ''
        frontal_vertical = ''
        preliminary_diagnosis = ''
        recommendation = ''

        for result in result_diagnostic:
            date_diagnostic = result.date
            user_name = result.user
            lateral_sagital = result.result_diagnostic['result_lateral_sag']
            lateral_vert = result.result_diagnostic['result_lateral_vert']
            frontal_hor = result.result_diagnostic['result_front_hor']
            frontal_vertical = result.result_diagnostic['result_front_vertical']
            preliminary_diagnosis = result.result_diagnostic['preliminary diagnosis']
            recommendation = result.result_diagnostic['recommendation']

        html = render_to_string('result_template/pdf_result.html',
                                {'date': date_diagnostic,
                                 'user_name': user_name,
                                 'result_lateral_sag': lateral_sagital,
                                 'result_lateral_vert': lateral_vert,
                                 'result_front_hor': frontal_hor,
                                 'result_front_vertical': frontal_vertical,
                                 'preliminary_diagnosis': preliminary_diagnosis,
                                 'recommendation': recommendation})

        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/base.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=stylesheets)
        email.attach(f'Result.pdf',
                     out.getvalue(),
                     'application/pdf')

        if request.POST.get('pdf') == '1':
            email.send()
            return render(request,
                          'result_template/list_result_type_photo.html',
                          context={'all_photo_diagnostics': all_photo_diagnostics}
                          )

        return render(request,
                      'result_template/result_photo.html',
                      context={'date': date_diagnostic,
                               'user_name': user_name,
                               'result_lateral_sag': lateral_sagital,
                               'result_lateral_vert': lateral_vert,
                               'result_front_hor': frontal_hor,
                               'result_front_vertical': frontal_vertical,
                               'preliminary_diagnosis': preliminary_diagnosis,
                               'recommendation': recommendation,
                               },

                      )

    return render(request,
                  'result_template/list_result_type_photo.html',
                  context={'all_photo_diagnostics': all_photo_diagnostics}
                  )
