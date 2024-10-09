from typing import Any
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template import Node


register = template.Library()

class RenderResults(Node):

    def __init__(self, suite):
        super().__init__()
        self.suite = suite

    def render(self, context):

        suite = self.suite.resolve(context)

        return self.render_accordion(suite['tests'])
    
    def render_accordion(self, items, level="0"):
        base_html = '<div class="accordion" id="results">\n'
        accordion_items = []
        end_html = '</div>\n'
        for idx , item in enumerate(items):
            bg_class = ""
            status = item.get("status", "")
            if status == "PASS":
                bg_class = "bg-success"
            elif status == "FAIL":
                bg_class = "bg-danger"

            item_init = f'<div class="accordion-item ">\n'
            item_head = f'<h2 class="accordion-header border-primary {bg_class}" id="result-heading-{level}-{idx}">\n'
            item_button = f'<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#result-{level}-{idx}" aria-expanded="true" aria-controls="result-{level}-{idx}">\n'
            if "name" in item:
                head = item["name"]
            elif "type" in item:
                head = item["type"]
            else:
                head = ""
            item_head_data = f'<p>{head}</p>\n'
            item_head_end = '</button>\n</h2>\n'
            item_body = f'<div id="result-{level}-{idx}" class="accordion-collapse collapse" aria-labelledby="result-heading-{level}-{idx}">\n'
            item_body_data = f'<div class="accordion-body">\n'
            attributes = ["name", "type", "doc", "start_time", "elapsed_time", "status", "assign", "args", "tags", "level", "message", "error"]       
            item_attrs_table = f'<table class="table table-hover attr-table">\n'
            item_attrs_data = ""
            for attr in attributes:
                if attr in item:
                    item_attrs_data += f'<tr>\n<th scope="row">{attr}</th>\n<td>{item[attr]}</td>\n</tr>\n'
            item_attrs_table += item_attrs_data + '</table>\n'
            item_body_data += item_attrs_table
            if "body" in item:
                item_body_data += self.render_accordion(item["body"], f"{level}-{idx}")
            item_body_end = '</div>\n</div>\n'
            item_end = '</div>\n'
            accordion_item = item_init + item_head + item_button + item_head_data + item_head_end + item_body + item_body_data  + item_body_end + item_end
            accordion_items.append(accordion_item)

        result = base_html + '\n'.join(accordion_items) + end_html
        return mark_safe(result)


@register.tag
def render_results(parser, token):
    bits = token.split_contents()
    bits.pop(0)
    suite = parser.compile_filter(bits.pop(0))
    result = RenderResults(suite)
    return result