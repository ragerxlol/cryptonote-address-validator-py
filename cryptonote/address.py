# Copyright (c) 2017 Michał Sałaban
# Copyright (c) 2016 The MoneroPy Developers
# Copyright (c) 2020, RagerX.lol
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from .base58 import decode
from .cn_utils import cn_fast_hash, encode_varint

KEY_SIZE = 32 * 2
ADDRESS_CHECKSUM_SIZE = 4 * 2
INTEGRATED_ID_SIZE = 8 * 2

def validate(address, prefixes, throw=False):
    addr_type = None
    prefix = None
    spend = None
    view = None
    pid = None
    checksum = None
    try:
        decodedAddr = decode(address)

        expectedPrefixReg = encode_varint(prefixes[0])
        expectedPrefixInt = encode_varint(prefixes[1])
        expectedPrefixSub = encode_varint(prefixes[2])

        expectedLengthReg = len(expectedPrefixReg) + KEY_SIZE + KEY_SIZE + ADDRESS_CHECKSUM_SIZE
        expectedLengthInt = len(expectedPrefixInt) + KEY_SIZE + KEY_SIZE + INTEGRATED_ID_SIZE + ADDRESS_CHECKSUM_SIZE
        expectedLengthSub = len(expectedPrefixSub) + KEY_SIZE + KEY_SIZE + ADDRESS_CHECKSUM_SIZE

        if decodedAddr.startswith(expectedPrefixReg) and len(decodedAddr) == expectedLengthReg:
            addr_type = 'regular'
            prefix    = decodedAddr[0 : len(expectedPrefixReg)]
            d         = decodedAddr[len(expectedPrefixReg) : ]
            spend     = d[0 : KEY_SIZE]
            view      = d[KEY_SIZE : KEY_SIZE + KEY_SIZE]
            checksum  = d[KEY_SIZE + KEY_SIZE : KEY_SIZE + KEY_SIZE + ADDRESS_CHECKSUM_SIZE]
            expectedChecksum = cn_fast_hash(prefix + spend + view)[0 : ADDRESS_CHECKSUM_SIZE]
        elif decodedAddr.startswith(expectedPrefixInt) and len(decodedAddr) == expectedLengthInt:
            addr_type = 'integrated'
            prefix    = decodedAddr[0 : len(expectedPrefixInt)]
            d         = decodedAddr[len(expectedPrefixInt) : ]
            spend     = d[0 : KEY_SIZE]
            view      = d[KEY_SIZE : KEY_SIZE + KEY_SIZE]
            pid       = d[KEY_SIZE + KEY_SIZE : KEY_SIZE + KEY_SIZE + INTEGRATED_ID_SIZE]
            checksum  = d[KEY_SIZE + KEY_SIZE + INTEGRATED_ID_SIZE : KEY_SIZE + KEY_SIZE + INTEGRATED_ID_SIZE + ADDRESS_CHECKSUM_SIZE]
            expectedChecksum = cn_fast_hash(prefix + spend + view + pid)[0 : ADDRESS_CHECKSUM_SIZE]
        elif decodedAddr.startswith(expectedPrefixSub) and len(decodedAddr) == expectedLengthSub:
            addr_type = 'sub'
            prefix    = decodedAddr[0 : len(expectedPrefixSub)]
            d         = decodedAddr[len(expectedPrefixSub) : ]
            spend     = d[0 : KEY_SIZE]
            view      = d[KEY_SIZE : KEY_SIZE + KEY_SIZE]
            checksum  = d[KEY_SIZE + KEY_SIZE : KEY_SIZE + KEY_SIZE + ADDRESS_CHECKSUM_SIZE]
            expectedChecksum = cn_fast_hash(prefix + spend + view)[0 : ADDRESS_CHECKSUM_SIZE]
        else:
            raise Exception('Invalid prefix')

        if checksum != expectedChecksum:
            raise Exception('Invalid checksum')

        return {
            'valid': True,
            'type': addr_type,
            'prefix': prefix,
            'spend': spend,
            'view': view,
            'pid': pid,
            'checksum': checksum
        }
    except:
        if throw:
            raise
        else:
            return {
                'valid': False,
                'type': None,
                'prefix': None,
                'spend': None,
                'view': None,
                'pid': None,
                'checksum': None
            }
