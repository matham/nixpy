# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import (absolute_import, division, print_function)

from . import util


class Entity(object):

    def __init__(self, h5group):
        util.check_entity_id(h5group.get_attr("entity_id"))
        self._h5group = h5group

    @classmethod
    def _create_new(cls, parent):
        id_ = util.create_id()
        h5group = parent.open_group(id_)
        h5group.set_attr("entity_id", id_)
        newentity = cls(h5group)
        newentity.force_created_at()
        newentity.force_updated_at()
        return newentity

    @property
    def id(self):
        return self._h5group.get_attr("entity_id")

    @property
    def created_at(self):
        return util.str_to_time(self._h5group.get_attr("created_at"))

    def force_created_at(self, t=util.now_int()):
        util.check_attr_type(t, int)
        self._h5group.set_attr("created_at", util.time_to_str(t))

    @property
    def updated_at(self):
        return util.str_to_time(self._h5group.get_attr("updated_at"))

    def force_updated_at(self, t=util.now_int()):
        util.check_attr_type(t, int)
        self._h5group.set_attr("updated_at", util.time_to_str(t))


class NamedEntity(object):

    def __init__(self, h5group):
        self._h5group = h5group
        # TODO: Validate object
        try:
            util.check_entity_name_and_type(h5group.get_attr("name"),
                                            h5group.get_attr("type"))
            util.check_entity_id(h5group.get_attr("entity_id"))
        except ValueError:
            ValueError("Invalid NIX object found in file.")

    @classmethod
    def _create_new(cls, parent, name, type_):
        util.check_entity_name_and_type(name, type_)
        h5group = parent.open_group(name)
        h5group.set_attr("name", name)
        h5group.set_attr("type", type_)
        h5group.set_attr("entity_id", util.create_id())
        newentity = cls(h5group)
        newentity.force_created_at()
        newentity.force_updated_at()
        return newentity

    @property
    def name(self):
        return self._h5group.get_attr("name")

    @property
    def type(self):
        return self._h5group.get_attr("type")

    @type.setter
    def type(self, t):
        if t is None:
            raise AttributeError("type can't be None")
        util.check_attr_type(t, str)
        self._h5group.set_attr("type", t)

    @property
    def definition(self):
        return self._h5group.get_attr("definition")

    @definition.setter
    def definition(self, d):
        util.check_attr_type(d, str)
        self._h5group.set_attr("definition", d)

    @property
    def id(self):
        return self._h5group.get_attr("entity_id")

    @property
    def created_at(self):
        return util.str_to_time(self._h5group.get_attr("created_at"))

    def force_created_at(self, t=util.now_int()):
        util.check_attr_type(t, int)
        self._h5group.set_attr("created_at", util.time_to_str(t))

    @property
    def updated_at(self):
        return util.str_to_time(self._h5group.get_attr("updated_at"))

    def force_updated_at(self, t=util.now_int()):
        util.check_attr_type(t, int)
        self._h5group.set_attr("updated_at", util.time_to_str(t))

    def __str__(self):
        return "{}: {{name = {}, type = {}, id = {}}}".format(
            type(self).__name__, self.name, self.type, self.id
        )

    def __repr__(self):
        return self.__str__()

