# -*- coding: utf-8 -*-
#
#   pyhwp : hwp file format parser in python
#   Copyright (C) 2010-2019 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from contextlib import contextmanager
import logging
import os
import tempfile

from zope.interface import implementer

from .interfaces import ITemporaryStreamFactory


logger = logging.getLogger(__name__)


@implementer(ITemporaryStreamFactory)
class TemporaryStreamFactory:

    @contextmanager
    def temporary_stream(self):
        fd, name = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'wb+') as fp:
                yield fp
        finally:
            try:
                os.unlink(name)
            except Exception as e:
                logger.warning('%s: can\'t unlink %s', e, name)
