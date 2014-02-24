# -*- coding: utf-8 -*-
#
#   pyhwp : hwp file format parser in python
#   Copyright (C) 2010-2014 mete0r <mete0r@sarangbang.or.kr>
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
from hwp5.binmodel._shared import RecordModel
from hwp5.tagids import HWPTAG_BIN_DATA
from hwp5.dataio import Enum
from hwp5.dataio import Flags
from hwp5.dataio import UINT16
from hwp5.dataio import Struct
from hwp5.dataio import BSTR
from hwp5.binmodel._shared import BinStorageId


class BinDataLink(Struct):
    def attributes():
        yield BSTR, 'abspath'
        yield BSTR, 'relpath'
    attributes = staticmethod(attributes)


class BinDataEmbedding(Struct):
    def attributes():
        yield BinStorageId, 'storage_id'
        yield BSTR, 'ext'
    attributes = staticmethod(attributes)


class BinDataStorage(Struct):
    def attributes():
        yield BinStorageId, 'storage_id'
    attributes = staticmethod(attributes)


class BinData(RecordModel):
    tagid = HWPTAG_BIN_DATA
    StorageType = Enum(LINK=0, EMBEDDING=1, STORAGE=2)
    CompressionType = Enum(STORAGE_DEFAULT=0, YES=1, NO=2)
    AccessState = Enum(NEVER=0, OK=1, FAILED=2, FAILED_IGNORED=3)
    Flags = Flags(UINT16,
                  0, 3, StorageType, 'storage',
                  4, 5, CompressionType, 'compression',
                  16, 17, AccessState, 'access')

    def attributes(cls):
        from hwp5.dataio import SelectiveType
        from hwp5.dataio import ref_member_flag
        yield cls.Flags, 'flags'
        yield (SelectiveType(ref_member_flag('flags', 'storage'),
                             {cls.StorageType.LINK: BinDataLink,
                              cls.StorageType.EMBEDDING: BinDataEmbedding,
                              cls.StorageType.STORAGE: BinDataStorage}),
               'bindata')
    attributes = classmethod(attributes)
