from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_email_pdf(request, result_diagnostic):
    print(request)
    email = EmailMessage(to=(request.user.email,))

    print(result_diagnostic)
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
        print(html)
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/base.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=stylesheets)
        email.attach(f'Result.pdf',
                     out.getvalue(),
                     'application/pdf')
        email.send()
        print("Compleate send")
