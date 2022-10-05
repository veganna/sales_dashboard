from django import template
from django.utils.safestring import mark_safe
from ..dashboardGeneric import GenericListMenu
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def create_generic_list_table(context):
    def format_item(field):
        try:
            return field.strftime('%m/%d/%Y')
        except:
            return field


    table = context['table']
    schema = context['schema']
    name = context['name']
    # create the table
    html = '<table class="table table-centered datatable dt-responsive nowrap" style="border-collapse: collapse; border-spacing: 0; width: 100%;">'
    # create the header
    html += '<thead class="thead-light"><tr><th style="width: 20px;"><div class="form-check"><input type="checkbox" class="form-check-input" id="customercheck"><label class="form-check-label mb-0" for="customercheck">&nbsp;</label></div></th>'
    for item in schema:
        html += '<th>' + item + '</th>'
    html += '<th style="width: 120px;">Action</th></tr></thead><tbody>'
    # create the body
    for item in table:
        html += '<tr><td><div class="form-check"><input type="checkbox" class="form-check-input" id="customercheck1"><label class="form-check-label mb-0" for="customercheck1">&nbsp;</label></div></td>'
        for key in schema:
            html += '<td>' + str(format_item(item[key])) + '</td>'
        html += f'<td id="tooltip-container1"><a href="{item["id"]}" class="me-3 text-primary" data-bs-container="#tooltip-container1" data-bs-toggle="tooltip" data-bs-placement="top" title="Edit"><i class="mdi mdi-pencil font-size-18"></i></a><a href="javascript:void(0);" onclick="delete_item({item["id"]})" class="text-danger" data-bs-container="#tooltip-container1" data-bs-toggle="tooltip" data-bs-placement="top" title="Delete"><i class="mdi mdi-trash-can font-size-18"></i></a></td></tr>'
    html += '</tboby></table>'

    return mark_safe(html)

@register.simple_tag(takes_context=True)
def create_generic_detail_form(context, request):
    html=''

    def define_type(input):
        if input['readonly']: return 'hidden'
        if input['type'] == 'DateTimeField' : return 'date'
        if input['type'] == 'IntegerField': return 'number'
        if input['type'] == 'TextField': return 'textarea'
        if input['type'] == 'CharField': return 'text'
        if input['type'] == 'ForeignKey': return 'select'
        if input['type'] == 'ManyToManyField': return 'select'
        if input['type'] == 'BooleanField': return 'checkbox'
        if input['type'] == 'DateField': return 'date'
        if input['type'] == 'ImageField': return 'file'
        return 'text'

    def define_value_simple(field, context):
        return context["model"][field]
        

    def define_value_foreign(field, context):
        field = f'{field}_id'
        return context["model"][field]
    
    def define_value_image(field, context):
        return context["model"][field].url

    def render_input_type_simple(input, context):
        return f'<input type="{define_type(input)}" name="{input["field"]}" value="{define_value_simple(input["field"], context)}"/>'

    def render_input_type_foreign(input, context):
        html = f'<select name="{input["field"]}" value="{define_value_foreign(input["field"], context)}">'
        obj = None
        for relation in range(len(context['relations'])):
            try:
                obj = context['relations'][relation][input['field']]
                break
            except:
                continue
        
        if not obj: return html+'</select>'

        for option in range(len(obj.all())):
            html += f'<option {"checked" if obj[option].id == define_value_foreign(input["field"], context) else "" } value="{obj[option].id}">{obj[option].__str__()}</option>'
        
        html += '</select>'
        return html

    def render_input_textarea(input, context):
        return f'<textarea name="{input["field"]}">{define_value_simple(input["field"], context)}</textarea>'
    
    def render_input_type_image(input, context):
        return f"<label>{input['name']}</label><br><img src='{define_value_image(input['field'], context)}' width='100px' height='100px' /><br><input type='file' name='{input['field']}' />"

    def render_input_type_boolean(input, context):
        return f'<input type="checkbox" name="{input["field"]}"/>'


    for item in range(len(context["form"])):
        if context["form"][item]["type"] == 'FileField' and context["form"][item]["value"].__class__.__name__ == 'ImageFieldFile':
            html += render_input_type_image(context["form"][item], context)
        elif context["form"][item]["type"] == 'ForeignKey':
            html += render_input_type_foreign(context["form"][item], context)
        elif context["form"][item]["type"] == 'TextField':
            html += render_input_textarea(context["form"][item], context)
        elif context["form"][item]["type"] == 'BooleanField':
            html += render_input_type_boolean(context["form"][item], context)
        else:
            html += render_input_type_simple(context["form"][item], context)

    
    request.session['relations'] = context['relations']

    return mark_safe(html)

@register.simple_tag(takes_context=True)
def render_generic_models(context):
    html = ''
    menu = GenericListMenu().build()
    for item in menu:
        html += f'<li><a href="/dashboard/{item["url"]}">{item["name"]}</a></li>'

    return mark_safe(html)
