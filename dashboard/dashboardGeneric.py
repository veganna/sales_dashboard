from .models import *


registerModel = [

]

class GenerateGenericList():
    def __init__(self):
        self.registedModels = registerModel
    
    def build(self, modelName=None, filters=[]):
        if not self.registedModels: return None
        if not modelName: return None

        def without_filter(self, modelName):
            for model in range(len(self.registedModels)):
                if modelName == self.registedModels[model].__name__:
                    return self.buildTable(self.registedModels[model].objects.all())

        def with_filter(self, modelName, filters):
            for model in range(len(self.registedModels)):
                if modelName == self.registedModels[model].__name__:
                    return self.buildTable(self.registedModels[model].objects.filter(**dict(filters)))

        if filters.__len__() == 0:
            return without_filter(self, modelName)

        return with_filter(self, modelName, filters)

    def buildTable(self, model):
        if not model: return None
        table = []
        
        for item in model:
            table.append(item.__dict__)

        for item in table:
            item.pop('_state')

        schema = self.buildSchema(table[0])

        name = model[0].__class__.__name__

        return {
            'schema': schema,
            'table': table,
            'name': name
        }

    def buildSchema(self, model):
        if not model: return None
        schema = []
        for key in model:
            schema.append(key)

        return schema

    def get_model_by_name(self, modelName):
        for model in self.registedModels:
            if model.__class__.__name__ == modelName:
                return model


class GenerateGenericDetail():
    def __init__(self):
        self.registedModels = registerModel

    def build(self, modelName=None, id=None):
        if not self.registedModels: return None
        if not modelName: return None
        if not id: return None

        for model in range(len(self.registedModels)):
            if modelName == self.registedModels[model].__name__:
                return self.buildForm(self.registedModels[model].objects.filter(id=id))

    def buildForm(self, model):
        if not model: return None
        form = []
        #create a dict with all the fields of the model[0] {field: value, name: name, type:type}
        for field in model[0]._meta.get_fields():
            try:
                #get if the field is readonly
                form.append({
                    'field': field.name,
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'readonly': False if field.editable else True,
                    'value': getattr(model[0], field.name)
                })

            except:
                pass
            
        #remove the id field
        form.pop(0)

        obj = model[0].__dict__
        obj.pop('_state')

        relations = []
        objRelations = []

        for field in model[0]._meta.get_fields():
            if field.is_relation:
                relations.append(field.name)
            
        for relation in relations:
            for model in range(len(self.registedModels)):
                if relation == self.registedModels[model].__name__.lower():
                    objRelations.append({relation:self.registedModels[model].objects.all()})

        return {
            'form': form,
            'model': obj,
            'relations': objRelations
        }

    def handler(self, modelName=None, id=None, fields=[]):
        if not self.registedModels: return None
        if not modelName: return None
        if not id: return None
        if not fields: return None

        for model in range(len(self.registedModels)):
            if modelName == self.registedModels[model].__name__:
                return self.update(self.registedModels[model].objects.filter(id=id), fields)

    def update(self, model, fields):
        if not model: return None
        if not fields: return None

        for field in fields:
            setattr(model[0], field[0], field[1])
        model[0].save()

        return self.buildForm(model)

    def delete(self, model):
        if not model: return None
        model[0].delete()

        return True

    def create(self, model, fields):
        if not model: return None
        if not fields: return None
        model[0].objects.create(**dict(fields))
        return True

    def create_form(self, model):
        if not model: return None
        form = []
        #create a dict with all the fields of the model[0] {field: value, name: name, type:type}
        for field in model[0]._meta.get_fields():
            try:
                form.append({
                    'field': field.name,
                    'name': field.verbose_name,
                    'type': field.get_internal_type(),
                    'readonly': field.readonly
                })
            except:
                pass
        #remove the id field
        form.pop(0)

        return {
            'form': form
        }

class GenericListMenu():
    def __init__(self):
        self.registedModels = registerModel

    def build(self):
        if not self.registedModels: return None
        menu = []
        for model in range(len(self.registedModels)):
            menu.append({
                'name': self.registedModels[model].__name__.capitalize(),
                'url': self.registedModels[model].__name__
            })

        return menu