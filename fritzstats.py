#!/usr/bin/env python3
#
# fritzswitch - Switch your Fritz!DECT200 via command line
#
# Copyright (C) 2014 Richard "Shred" Körber
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import hashlib
import urllib
import json
from pprint import pprint
from urllib.request import urlopen
from xml.etree.ElementTree import parse

class FritzStats:
    def __init__(self, user, password, url):
        """Create a connection to the Fritz!Box with the given user and password."""
        self.fritzurl = url
        self.sid = self.get_sid(user, password)

    def get_sid(self, user, password):
        """Authenticate and get a Session ID"""
        with urlopen(self.fritzurl + '/login_sid.lua') as f:
            dom = parse(f)
            sid = dom.findtext('./SID')
            challenge = dom.findtext('./Challenge')
            
        if sid == '0000000000000000':
            md5 = hashlib.md5()
            md5.update(challenge.encode('utf-16le'))
            md5.update('-'.encode('utf-16le'))
            md5.update(password.encode('utf-16le'))
            response = challenge + '-' + md5.hexdigest()
            uri = self.fritzurl + '/login_sid.lua?username=' + user + '&response=' + response
            with urlopen(uri) as f:
                dom = parse(f)
                sid = dom.findtext('./SID')

        if sid == '0000000000000000':
            raise PermissionError('access denied')

        return sid

    def get_stats(self):
        data={"xhr": "1", "lang": "de", "xhldr": "all", "page": "ecoStat", "sid": self.sid }
        data = urllib.parse.urlencode(data)
        data = data.encode('ascii')

        with urlopen(self.fritzurl + '/data.lua', data=data) as f:
            res = f.read().decode('utf-8')
            res = json.loads(res)
        # pprint(res)
        cputemp = res["data"]["cputemp"]["series"][0][-1]
        # print("cputemp =", cputemp)
        cpuutil = res["data"]["cpuutil"]["series"][0][-1]
        # print("cpuutil =", cpuutil)
        ramusage = res["data"]["ramusage"]["series"]
        ram_fixed = ramusage[0][-1]
        ram_dynamic = ramusage[1][-1]
        ram_free = ramusage[2][-1]
        # print("ramusage(fixed, dynamic, free)% =", ram_fixed, ram_dynamic, ram_free)
        return cputemp, cpuutil, ram_fixed, ram_dynamic, ram_free
