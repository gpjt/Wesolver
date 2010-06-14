import json

from django.db import models

from django.contrib.auth.models import User


class Worksheet(object):
    def __init__(self, model):
        self.model = model
        self.max_col = 10
        self.max_row = 10
        for (col, row) in self.model:
            if col > self.max_col:
                self.max_col = col
            if row > self.max_row:
                self.max_row = row

    def recalc(self):
        context = {}

        self.header_code = "worksheet = {}"
        exec(self.header_code, context)

        constants = []
        expressions = []
        for k, v in self.model.items():
            if v.startswith("="):
                expressions.append((k, v))
            else:
                constants.append("worksheet[%s] = %s" % (k, v))
        self.constants_and_formatting = "\n".join(constants)
        exec(self.constants_and_formatting, context)

        formulae = []
        for k, v in expressions:
            formula = "worksheet[%s] = %s" % (k, v[1:])
            try:
                exec(formula, context)
                formulae.append(formula)
            except Exception, e:
                formulae.append("# Error executing %s\n# %s" % (formula, e))
                context["worksheet"][k] = "#ERR"
        self.formulae = "\n".join(formulae)

        self.results = context["worksheet"]
        print "Spreadsheet recalculated, results are %s" % self.results



class Spreadsheet(models.Model):

    owner = models.ForeignKey(User)

    name = models.CharField(max_length=255)

    contents = models.TextField()


    def worksheet(self):
        model = {}
        if self.contents and not self.contents == ".":
            model = eval(self.contents)
        return Worksheet(model)


    def update(self, (col, row), value):
        worksheet = self.worksheet()
        if value == '':
            del worksheet.model[col, row]
        else:
            worksheet.model[col, row] = value
        self.contents = str(worksheet.model)


    def json(self):
        worksheet = self.worksheet()
        worksheet.recalc()
        modelRows = []
        resultRows = []
        for row in range(1, worksheet.max_row + 1):
            modelCols = []
            resultCols = []
            for col in range(1, worksheet.max_col + 1):
                modelCols.append(worksheet.model.get((col, row), ""))
                resultCols.append(worksheet.results.get((col, row), ""))
            modelRows.append(modelCols)
            resultRows.append(resultCols)
        jsonObject = {
            "model" : modelRows,
            "result" : resultRows,
            "header_code" : worksheet.header_code,
            "constants_and_formatting" : worksheet.constants_and_formatting,
            "formulae" : worksheet.formulae
        }

        return json.dumps(jsonObject)


    def __unicode__(self):
        return "[%s] %s" % (self.owner, self.name)
