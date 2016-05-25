#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 SKA South Africa
#
# This file is part of hypercube.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from copy import (copy as shallow_copy,
    deepcopy)

from attrdict import AttrDict
import numpy as np

DEFAULT_DESCRIPTION = 'The FOURTH dimension!'

def create_dimension(name, dim_data, **kwargs):
    if isinstance(dim_data, Dimension):
        dim = deepcopy(dim_data)
        dim.update(**kwargs)
    else:
        dim = Dimension(name, dim_data, **kwargs)

    return dim

class Dimension(object):
    __slots__ = ['_name', '_global_size', '_local_size',
        '_lower_extent', '_upper_extent',
        '_description', '_zero_valid']

    def __init__(self, name, global_size, local_size=None,
            lower_extent=None, upper_extent=None,
            description=None,
            zero_valid=True):
        """
        Create a dimension data dictionary from supplied argument
        """
        super(Dimension, self).__init__()

        self._name = name
        self._global_size = global_size
        self._local_size = local_size or global_size
        self._lower_extent = lower_extent or (global_size
                if isinstance(global_size, str) else 0)
        self._upper_extent = upper_extent or global_size
        self._description = description or DEFAULT_DESCRIPTION
        self._zero_valid = zero_valid

    @property
    def name(self):
        return self._name
    
    @property
    def global_size(self):
        return self._global_size

    @property
    def local_size(self):
        return self._local_size
    
    @property
    def lower_extent(self):
        return self._lower_extent
    
    @property
    def upper_extent(self):
        return self._upper_extent
    
    @property
    def extent_size(self):
        return self.upper_extent - self.lower_extent
    
    @property
    def description(self):
        return self._description

    @property
    def zero_valid(self):
        return self._zero_valid

    def update(self, local_size=None,
        lower_extent=None, upper_extent=None,
        description=None, zero_valid=None):

        self._local_size = local_size or self._local_size
        self._lower_extent = lower_extent or self._lower_extent
        self._upper_extent = upper_extent or self._upper_extent
        self._description = description or self._description
        self._zero_valid = zero_valid or self._zero_valid

        # Check that we've been given valid values
        self.validate()

    def is_expression(self):
        return (isinstance(self._global_size, str) or
            isinstance(self._local_size, str) or
            isinstance(self._lower_extent, str) or 
            isinstance(self._upper_extent, str))

    def validate(self):
        """ Validate the contents of a dimension data dictionary """

        # Currently, we don't validate string expressions
        if self.is_expression():
            return

        # Sanity validate dimensions
        if self._local_size > self._global_size:
            raise ValueError("Dimension '{n}' "
                "local size {l} is greater than "
                "it's global size {g}".format(n=self._name,
                    l=self._local_size, g=self._global_size))

        if self._upper_extent - self._lower_extent > self._local_size:
            raise ValueError("Dimension '{n}' "
                "extent range [{el}, {eu}] ({r}) "
                "is greater than it's local size {l}. "
                "If this dimension is defined as "
                "an expression containing multiple "
                "dimensions, these extents may be "
                "much larger than the local size. "
                "Consider forcing the extents "
                "to [0,1] as meaningful extents "
                "are unlikely in these cases.".format(
                    n=name, l=ls,
                    el=self.lower_extent, eu=self.upper_extent,
                    r=self.upper_extent - self.lower_extent))

        if self.zero_valid:
            assert (0 <= self.lower_extent <= self.upper_extent
                <= self.global_size), (
                "Dimension '{d}', global size {gs}, extents [{el}, {eu}]"
                    .format(d=self.name, gs=self.global_size,
                        el=self.lower_extent, eu=self.upper_extent))
        else:
            assert (0 < self.lower_extent <= self.upper_extent
                <= self.global_size), (
                "Dimension '{d}', global size {gs}, extents [{el}, {eu}]"
                    .format(d=self.name, gs=self.global_size,
                        el=self.lower_extent, eu=self.upper_extent))

    def __str__(self):
        return ("['{n}': global: {gs} local: {ls} "
            "lower: {el} upper: {eu}]").format(
                n=self.name, gs=self.global_size, ls=self.local_size,
                el=self.lower_extent, eu=self.upper_extent)

