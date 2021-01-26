import time
import datetime
import os

from django.http.response import HttpResponse
from django.utils.http import urlquote
from django.utils.encoding import smart_text
from django.conf import settings


class TxtExport(object):

    def __init__(self, datas, fields='__all__', headers=None, filename=None):
        self.datas = datas
        self.fields = fields
        self.headers = headers
        self.filename = filename
        self.total = len(self.datas)
        self.counter = 0

        if not isinstance(self.filename, str):
            self.filename = '%s_export.txt' % time.strftime("%Y%m%d_%H%M%S")

        if self.fields == '__all__':
            self.fields = []
            if len(self.datas):
                if isinstance(self.datas[0], dict):
                    self.fields = list(self.datas[0].keys())

    def get_response(self):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment;filename=%s' % urlquote(self.filename)
        split_char = ','
        line_end = '\n'
        if self.headers:
            response.write(split_char.join(self.headers) + line_end)
        for data in self.datas:
            row_str = split_char.join(
                ([str('' if data.get(field) is None else data.get(field))
                  for field in self.fields]))
            response.write(row_str + line_end)

        return response

    def save_file(self, basedir=None):
        from mysite.tools.export_utils.utils import get_field_value
        if not basedir:
            basedir = os.path.join(settings.FILES_ROOT, 'reports')
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        basedir = os.path.join(basedir, datetime.datetime.now().strftime('%Y%m%d'))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filepath = os.path.abspath(os.path.join(basedir, smart_text(self.filename)))
        split_char = ','
        line_end = '\n'
        with open(filepath, 'w', encoding='utf8') as f:
            if self.headers:
                f.write(split_char.join(self.headers) + line_end)
            for data in self.datas:
                row_str = split_char.join(
                    ([get_field_value(data, field).replace(',', ';')
                      for field in self.fields]))
                f.write(row_str + line_end)
        return filepath
