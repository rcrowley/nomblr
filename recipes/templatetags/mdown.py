from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django import template

import markdown

# Monkey patch the Markdown library to more strictly handle lists.  There's
# nothing in Gruber's spec about mixing list syntax and it makes two lists
# with nothing in between run together with sporadic <p> tags.  No bueno.
import markdown.blockprocessors
import re
def run(self, parent, blocks):
    # Check fr multiple items in one block.
    items = self.get_items(blocks.pop(0))
    sibling = self.lastChild(parent)
    if sibling and self.TAG == sibling.tag: # XXX This is the change.
        # Previous block was a list item, so set that as parent
        lst = sibling
        # make sure previous item is in a p.
        if len(lst) and lst[-1].text and not len(lst[-1]):
            p = markdown.util.etree.SubElement(lst[-1], 'p')
            p.text = lst[-1].text
            lst[-1].text = ''
        # parse first block differently as it gets wrapped in a p.
        li = markdown.util.etree.SubElement(lst, 'li')
        self.parser.state.set('looselist')
        firstitem = items.pop(0)
        self.parser.parseBlocks(li, [firstitem])
        self.parser.state.reset()
    else:
        # This is a new list so create parent with appropriate tag.
        lst = markdown.util.etree.SubElement(parent, self.TAG)
    self.parser.state.set('list')
    # Loop through items in block, recursively parsing each with the
    # appropriate parent.
    for item in items:
        if item.startswith('   '): # XXX Used to reference markdown.TAB_LENGTH.
            # Item is indented. Parse with last item as parent
            self.parser.parseBlocks(lst[-1], [item])
        else:
            # New item. Create li and parse with it as parent
            li = markdown.util.etree.SubElement(lst, 'li')
            self.parser.parseBlocks(li, [item])
    self.parser.state.reset()
setattr(markdown.blockprocessors.OListProcessor, 'run', run)
setattr(markdown.blockprocessors.OListProcessor,
        'CHILD_RE',
        re.compile(r'^[ ]{0,3}((\d+\.))[ ]+(.*)'))
setattr(markdown.blockprocessors.UListProcessor,
        'CHILD_RE',
        re.compile(r'^[ ]{0,3}(([*+-]))[ ]+(.*)'))

register = template.Library()

@register.filter
@stringfilter
def mdown(value):
    return mark_safe(markdown.markdown(value))
