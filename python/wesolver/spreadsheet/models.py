try:
    import json
except ImportError:
    import simplejson as json
import re

from django.db import models

from django.contrib.auth.models import User


FLOAT_RE = r'(?:[0-9]*\.[0-9]+|[0-9]+\.[0-9]*)'
INT_RE = r'[1-9][0-9]*'
CELLREF_RE = r'([A-Za-z])([1-9][0-9]*)'


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


    def exec_formula(self, location, expressions, context, formulae, done):
        if location in done:
            return

        try:
            expression = expressions[location][1:]
        except KeyError:
            return

        formula = "worksheet[%s] = " % (location, )
        while True:
            match = re.search(CELLREF_RE, expression)
            if not match:
                break

            formula += expression[:match.start()]
            dependencyLocation = (ord(match.group(1).upper()) - 64, int(match.group(2)))
            formula += "worksheet[%s, %s]" % dependencyLocation
            self.exec_formula(dependencyLocation, expressions, context, formulae, done)

            expression = expression[match.end():]
        formula += expression

        try:
            exec(formula, context)
            formulae.append(formula)
        except Exception, e:
            formulae.append("# Error executing %s\n# %s" % (formula, e))
            context["worksheet"][location] = "#ERR"

        done.add(location)


    def walk_formulae(self, expressions, context):
        return formulae


    def recalc(self, pre_constants_user_code, pre_formula_user_code, post_formula_user_code):
        context = {}

        self.header_code = "worksheet = {}"
        exec(self.header_code, context)

        exec(pre_constants_user_code, context)

        constants = []
        expressions = {}
        for k, v in self.model.items():
            if v.startswith("="):
                expressions[k] = v
            else:
                if not re.match(FLOAT_RE, v) and not re.match(INT_RE, v):
                    v = "'%s'" % v
                constants.append("worksheet[%s] = %s" % (k, v))
        self.constants_and_formatting = "\n".join(constants)
        exec(self.constants_and_formatting, context)

        exec(pre_formula_user_code, context)

        formulae = []
        done = set()
        for location in expressions:
            self.exec_formula(location, expressions, context, formulae, done)
        self.formulae = "\n".join(formulae)

        exec(post_formula_user_code, context)

        self.results = context["worksheet"]



class Spreadsheet(models.Model):

    owner = models.ForeignKey(User)

    name = models.CharField(max_length=255)

    contents = models.TextField(blank=True)

    pre_constants_user_code = models.TextField(blank=True)

    pre_formula_user_code = models.TextField(blank=True)

    post_formula_user_code = models.TextField(blank=True)



    def worksheet(self):
        model = {}
        if self.contents:
            model = eval(self.contents)
        return Worksheet(model)


    def update(self, (col, row), value):
        worksheet = self.worksheet()
        if value == '':
            del worksheet.model[col, row]
        else:
            worksheet.model[col, row] = value
        self.contents = str(worksheet.model)


    def update_user_code(self, section, value):
        if section == "pre_constants_user_code":
            self.pre_constants_user_code = value
        elif section == "pre_formula_user_code":
            self.pre_formula_user_code = value
        elif section == "post_formula_user_code":
            self.post_formula_user_code = value


    def json(self):
        worksheet = self.worksheet()
        worksheet.recalc(self.pre_constants_user_code, self.pre_formula_user_code, self.post_formula_user_code)
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
            "formulae" : worksheet.formulae,
            "pre_constants_user_code" : self.pre_constants_user_code,
            "pre_formula_user_code" : self.pre_formula_user_code,
            "post_formula_user_code" : self.post_formula_user_code,
        }

        return json.dumps(jsonObject)


    def __unicode__(self):
        return "[%s] %s" % (self.owner, self.name)
