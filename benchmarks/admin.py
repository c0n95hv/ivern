# Register your models here.
import json
import os
import re
import zipfile

from django.contrib import admin

from benchmarks.models import LogFile, Project, Drive, Case
from ivern import settings

EXTRACTED_PATH = 'data'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'smart_before_test_path', 'smart_after_test_path', 'upload')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        zip_file = os.path.join(settings.MEDIA_ROOT, str(obj.upload))
        directory_to_extract = os.path.join(settings.MEDIA_ROOT, EXTRACTED_PATH)
        name_list = []
        if zipfile.is_zipfile(zip_file):
            with zipfile.ZipFile(zip_file) as zip_object:
                name_list = zip_object.namelist()
                zip_object.extractall(directory_to_extract)

        project = Project.objects.get(id=obj.id)
        drive = Drive.objects.filter(project__name=project.name)
        drive.delete()

        for name in name_list:
            new_name = os.path.join(EXTRACTED_PATH, name)
            if name.endswith('SMART_Before_Test.txt'):
                project.smart_before_test_path.name = new_name
            if name.endswith('SMART_After_Test.txt'):
                project.smart_after_test_path.name = new_name
            project.save()

        for name in name_list:
            if re.compile('/sd.*/$').search(name):
                drive = Drive.objects.create(project=project, name=name.split('/')[1])
                drive.save()

        for name in name_list:
            new_name = os.path.join(EXTRACTED_PATH, name)
            if name.endswith('.log') and not name.endswith('.1.log'):
                item = name.split('/')
                drive = project.drive_set.get(name=item[1])
                with open(os.path.join(settings.MEDIA_ROOT, EXTRACTED_PATH, name)) as f:
                    case = Case.objects.create(
                        drive=drive, name=item[2].strip('.log'), result=json.load(f), path=new_name
                    )
                    case.save()

        for name in name_list:
            new_name = os.path.join(EXTRACTED_PATH, name)
            if name.endswith('.1.log'):
                item = name.split('/')
                drive = project.drive_set.get(name=item[1])
                case = drive.case_set.get(name='_'.join(item[2].split('.')[0].split('_')[:-1]))
                log_file = LogFile.objects.create(case=case, name=item[2], path=new_name)
                log_file.save()

        #         with open(os.path.join(settings.MEDIA_ROOT, 'data', name)) as f:
        #             for line in f.readlines():
        #                 value = line.split(',')
        #                 print(line)
        #                 LogFileContent.objects.create(
        #                     time=value[0], value=value[1], data_direction=value[2], log_file=log_file
        #                 ).save()


class DriveAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name')
    search_fields = ('name',)
    list_filter = ('project',)
    autocomplete_fields = ['project']


class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'drive', 'result', 'path')
    search_fields = ('name',)
    list_filter = ('drive',)
    autocomplete_fields = ['drive']


class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'case', 'path')
    search_fields = ('name', 'path')
    list_filter = ('case',)
    autocomplete_fields = ['case']


class LogFileContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'value', 'data_direction', 'block_size', 'offset', 'command_priority', 'log_file')
    autocomplete_fields = ['log_file']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Drive, DriveAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(LogFile, LogFileAdmin)
# admin.site.register(LogFileContent, LogFileContentAdmin)
