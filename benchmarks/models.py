from django.db import models


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=128)
    smart_before_test_path = models.FileField(blank=True, null=True, verbose_name='Pre S.M.A.R.T Info ')
    smart_after_test_path = models.FileField(blank=True, null=True, verbose_name='Post S.M.A.R.T Info ')
    upload = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Project'


class Drive(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    class Meta:
        verbose_name = 'Drive'


class Case(models.Model):
    name = models.CharField(max_length=128)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    result = models.JSONField(blank=True, null=True)
    path = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.drive.project.name} - {self.drive.name} - {self.name}"

    class Meta:
        verbose_name = 'Case'


class LogFile(models.Model):
    name = models.CharField(max_length=128)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, db_index=True)
    path = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.case.drive.project.name} - {self.case.drive.name} - {self.case.name} - {self.name}"

    class Meta:
        verbose_name = 'LogFile'


# class LogFileContent(models.Model):
#     """
#     https://fio.readthedocs.io/en/latest/fio_doc.html#log-file-formats
#
#     Fio supports a variety of log file formats, for logging latencies, bandwidth, and IOPS.
#     The logs share a common format, which looks like this:
#         time (msec), value, data direction, block size (bytes), offset (bytes), command priority
#     """
#     time = models.IntegerField()
#     value = models.BigIntegerField()
#     data_direction = models.SmallIntegerField()
#     block_size = models.SmallIntegerField(default=0)
#     offset = models.SmallIntegerField(default=0)
#     command_priority = models.SmallIntegerField(default=0)
#
#     log_file = models.ForeignKey(LogFile, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'LogFileContent'
from django.db import models
