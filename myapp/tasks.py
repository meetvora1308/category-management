from io import BytesIO

import openpyxl
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


@shared_task
def schedule_email_task(email):
    users = User.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"

    # Append the header row
    ws.append(["ID", "Username", "Is Active"])

    # Append user data
    for user in users:
        ws.append([user.id, user.username, user.is_active])

    # Save the workbook to a BytesIO buffer
    file_buffer = BytesIO()
    wb.save(file_buffer)
    file_buffer.seek(0)
    mail = EmailMessage("User Data", "Please find the attached user data.", to=[email])
    mail.attach(
        "users.xlsx",
        file_buffer.getvalue(),
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    mail.send()
