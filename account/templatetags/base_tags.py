from django import template

register = template.Library()


@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, classes, content):
    return {
        'request': request,
        'link_name': link_name,
        'link': "account:{}".format(link_name),
        'content': content,
        'classes': classes,
    }


@register.inclusion_tag("registration/partials/link2.html")
def link2(request, link_name, classes, content):
    return {
        'request': request,
        'link_name': link_name,
        'link': "tweet:{}".format(link_name),
        'content': content,
        'classes': classes,
    }
