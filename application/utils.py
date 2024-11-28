import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from .models import Attendance, Group
from datetime import datetime
import os

class AttendanceReportGenerator:

    @staticmethod
    def process_attendance_data(groups, date):
        # Получаем студентов по выбранным группам и указанной дате
        attendances = Attendance.objects.filter(date=date, student__student_group__in=groups).values('student__user_full_name', 'morning_status', 'lunch_status', 'lateness', 'student__student_group')

        student_records = {}
        for record in attendances:
            student_name = record['student__user_full_name']
            group = record['student__student_group']
            morning_status = record['morning_status']
            lunch_status = record['lunch_status']
            lateness = record['lateness']
            
            if student_name not in student_records:
                student_records[student_name] = {
                    'Утро': morning_status or 'Не пришел',
                    'Обед': lunch_status or 'Не пришел',
                    'ГРУППА': group,
                    'Время утро': morning_status,
                    'Время обед': lunch_status,
                    'Опоздание': '+' if lateness else ''
                }
            
            # Применяем логику для утреннего и обеденного времени
            if morning_status is None:
                student_records[student_name]['Утро'] = 'Не пришел'
            if lunch_status is None:
                student_records[student_name]['Обед'] = 'Не пришел'
            
            if lateness:
                student_records[student_name]['Опоздание'] += '+'

        # Преобразуем в DataFrame
        df = pd.DataFrame.from_dict(student_records, orient='index')
        df['Дата'] = date
        return df

    @staticmethod
    def generate_report(request):
        # Получаем дату и список выбранных групп
        date_str = request.GET.get('date')
        groups = request.GET.getlist('groups')  # Получаем список групп
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Обрабатываем данные
        df = AttendanceReportGenerator.process_attendance_data(groups, date)

        # Сохраняем файл в директорию 'media/reports'
        report_dir = os.path.join('media', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        # Генерация XLSX
        groups_str = "_".join(groups)
        report_filename = f"Посещаемость {groups_str} {date}.xlsx"
        report_path = os.path.join(report_dir, report_filename)
        df.to_excel(report_path, index=False)

        # Отправляем ссылку на созданный файл
        return HttpResponse(f"Отчет успешно создан! Скачайте его по <a href='/media/reports/{report_filename}'>ссылке</a>.")
