from django import template

register = template.Library()

@register.filter
def number_to_month(value):
    print(value)
    months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]
    return months[value-1]