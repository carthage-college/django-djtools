from django.template import loader
from django.http import HttpResponse
from django.utils.encoding import smart_bytes

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from io import BytesIO

import csv

def create_workbook(workbook, template, data, filename, delimiter):
    wb = load_workbook(workbook)
    ws = wb.active
    # this could all be accomplished by a list of lists but building a list
    # for each row would be ugly. this seems more pythonic, and we can reuse
    # for CSV export if need be.
    t = loader.get_template(template)
    rendered = smart_bytes(
        t.render(data), encoding='utf-8', strings_only=False, errors='strict'
    )
    # reader requires an object which supports the iterator protocol and
    # returns a string each time its next() method is called. StringIO
    # provides an in-memory, line by line stream of the template data.
    #reader = csv.reader(io.StringIO(rendered), delimiter="|")
    reader = csv.reader(BytesIO(rendered), delimiter="|")
    for row in reader:
        ws.append(row)

    # in memory response instead of save to file system
    response = HttpResponse(
        save_virtual_workbook(wb), content_type='application/ms-excel'
    )

    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(
        filename
    )

    return response
