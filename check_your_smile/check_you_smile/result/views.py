from django.shortcuts import render, get_object_or_404
from .models import ResultDiagnostic
from diagnostic.models import Diagnostic
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django_celery_results.models import TaskResult
import json


# Create your views here.


def load_result(request, diagnostic_slug=None):
    diagnostic = None
    diagnostics = Diagnostic.objects.all()
    task_result = TaskResult.objects.all()
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
        # task_result = TaskResult.objects.get(task_id='b89e3aae-f368-4c0c-8155-9ac79bc40362').result
        # task_json = json.loads(task_result.replace('\'', '"'))


        date_diagnostic = ''
        user_name = ''
        lateral_sagital = ''
        lateral_vert = ''
        frontal_hor = ''
        frontal_vertical = ''
        preliminary_diagnosis = ''
        recommendation = ''

        for result in result_diagnostic:
            task_result = TaskResult.objects.get(task_id=result.result_diagnostic).result
            task_json = json.loads(task_result.replace('\'', '"'))
            date_diagnostic = result.date
            user_name = result.user
            lateral_sagital = task_json['result_lateral_sag']
            lateral_vert = task_json['result_lateral_vert']
            frontal_hor = task_json['result_front_hor']
            frontal_vertical = task_json['result_front_vertical']
            preliminary_diagnosis = task_json['preliminary diagnosis']
            recommendation = task_json['recommendation']

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
