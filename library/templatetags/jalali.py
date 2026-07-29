from django import template
import jdatetime

register = template.Library()

@register.filter
def jalali(value):
    if not value:
        return ""

    return jdatetime.datetime.fromgregorian(datetime=value).strftime("%Y/%m/%d %H:%M")
