##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import component, interface, schema

from z3c.form import converter
from z3c.form.browser import textarea
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget
from zojax.widget.list.interfaces import IList


class ListWidget(textarea.TextAreaWidget):

    rows = 6


class ListDataConverter(converter.BaseDataConverter):
    """
    >>> from zojax.widget.list import SimpleList
    >>> list = SimpleList()

    >>> converter = ListDataConverter(list, None)

    >>> converter.toWidgetValue(None)
    u''

    >>> print converter.toWidgetValue(['line1', 'line2', 'line3'])
    line1
    line2
    line3

    >>> print converter.toFieldValue('line5 \\n line8\\n line10')
    ['line5', 'line8', 'line10']

    >>> ListFieldWidget(list, None)
    <ListWidget ''>
    """

    component.adapts(schema.interfaces.IList, ListWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return '\n'.join(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        field = self.field
        if field.value_type is not None:
            tp = getattr(field.value_type, '_type', unicode)
            value = [tp(elem.strip()) for elem in value.split('\n') if elem]
        else:
            value = [elem.strip() for elem in value.split('\n') if elem]

        if hasattr(self.field, '_type'):
            return self.field._type(value)
        else:
            return value


@interface.implementer(IFieldWidget)
@component.adapter(IList, IFormLayer)
def ListFieldWidget(field, request):
    return FieldWidget(field, ListWidget(request))
