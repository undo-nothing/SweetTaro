import time

from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.admin.utils import label_for_field

from apps.utils.export import TxtExport, CsvExport


class ExportModelMixin(object):
    export_headers = None

    def get_export_data(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        print(request.query_params)
        if not request.query_params.get('export_all') == 'true':
            queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    def get_headers_translation(self, export_headers):
        translated_headers = []
        label_dict = {}
        if hasattr(self, 'get_serializer'):
            fields = self.get_serializer().fields
            label_dict = {name: str(field.label) for name, field in list(fields.items()) if field.label}

        for name in export_headers:
            if name in label_dict:
                translated_headers.append(label_dict[name])
            elif hasattr(self, 'model'):
                try:
                    translated_headers.append(label_for_field(name, self.model))
                except AttributeError:
                    translated_headers.append(name.replace('_', ' ').capitalize())

        return translated_headers

    def get_file_title(self):
        return self.basename

    def get_filename(self, filename=None, suffix=''):
        if not isinstance(filename, str):
            filename = '%s_%s' % (self.get_file_title(), time.strftime("%Y%m%d%H%M%S"))
        if suffix and len(filename.split('.')) == 1:
            filename = "%s.%s" % (filename, suffix.strip('.'))

        return filename

    def export_to_txt(self, export_headers, datas, file_name=None, as_file=False):
        translated_headers = self.get_headers_translation(export_headers)
        file_name = self.get_filename(file_name, 'txt')
        txt_handle = TxtExport(datas, export_headers, translated_headers, file_name)
        if as_file:
            return txt_handle.save_file()
        response = txt_handle.get_response()
        return response

    def export_to_csv(self, export_headers, datas, file_name=None, as_file=False):
        translated_headers = self.get_headers_translation(export_headers)
        file_name = self.get_filename(file_name, 'csv')
        csv_handle = CsvExport(datas, export_headers, translated_headers, file_name)
        if as_file:
            return csv_handle.save_file()
        response = csv_handle.get_response()
        return response

    @action(methods=['get'], detail=False)
    def export(self, request, async_task=True, recorder=None):
        self.export_headers = self.export_headers = request.query_params.get('export_headers', "").split(",")
        file_format = request.query_params.get('export_type', '')
        if file_format not in ('csv', 'txt', 'xls', 'pdf'):
            message = 'export_type required and must in csv txt xls pdf'
            return Response({'code': -1, 'message': message}, status=400)

        export_data = self.get_export_data(request)
        data_fields = list(export_data[0].keys()) if len(export_data) else []
        headers_list = []
        for header in self.export_headers:
            if header in data_fields:
                headers_list.append(header)
        self.export_headers = headers_list
        if file_format == 'csv':
            return self.export_to_csv(self.export_headers, export_data)
        elif file_format == 'xls':
            return self.export_to_xls(self.export_headers, export_data)
        elif file_format == 'txt':
            return self.export_to_txt(self.export_headers, export_data)
        elif file_format == 'pdf':
            return self.export_to_pdf(self.export_headers, export_data)
        else:
            return self.export_to_csv(self.export_headers, export_data)
