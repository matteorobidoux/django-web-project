from django import template
register = template.Library()

@register.filter(name='nonpage_attributes')
def get_nonpage_attributes(request):
    attributes = ''
    for (key, value) in request.GET.items():
        if key!='page':
            attributes += f'&{key}={value}'

    return attributes