import markdown

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def convert_markdown(value):
    return markdown.markdown(value)


from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False

@register.filter
def unmark(text):
    return __md.convert(text)