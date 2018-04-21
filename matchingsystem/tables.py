import django_tables2 as tables
from .models import Project_assignment
from django_tables2.export.views import ExportMixin

# Defines the view for the results of the matching algorithm

class ResultTable(tables.Table):
	export_formats = ['csv', 'xls']

	class Meta:
		model = Project_assignment
		template = 'django_tables2/bootstrap.html'

class TableView(ExportMixin, tables.SingleTableView):
    table_class = ResultTable
    model = Project_assignment
template_name = 'django_tables2/bootstrap.html'
