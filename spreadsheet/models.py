from django.db import models

from django.contrib.auth.models import User



class Worksheet(object):
    def __init__(self, dict):
        self.dict = dict
        self.max_col = 0
        self.max_row = 0
        for (col, row) in self.dict:
            if col > self.max_col:
                self.max_col = col
            if row > self.max_row:
                self.max_row = row



class Spreadsheet(models.Model):

    owner = models.ForeignKey(User)

    name = models.CharField(max_length=255)

    contents = models.TextField()
    

    def worksheet(self):
        return Worksheet({ (1, 1) : 10, (2, 2): "hello" })


    def json(self):
        worksheet = self.worksheet()
        rows = []
        for row in range(1, worksheet.max_row + 1):
            cols = []
            for col in range(1, worksheet.max_col + 1):
                cols.append('"%s"' % (worksheet.dict.get((col, row), "")))
            rows.append("[" + ",".join(cols) + "]")
        return "[" + ",\n".join(rows) + "]"


    def __unicode__(self):
        return "[%s] %s" % (self.owner, self.name)
