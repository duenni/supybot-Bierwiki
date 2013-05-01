# -*- coding: utf-8 -*-
###
# Copyright (c) 2013, duenni
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import re
import lxml.html
import lxml.cssselect
import itertools
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('Bierwiki')

@internationalizeDocstring
class Bierwiki(callbacks.Plugin):
    """Add the help for "@plugin help Bierwiki" here
    This should describe *how* to use this plugin."""
    threaded = True
    
    def bwlink(self, irc, msg, args, searchterm):
        """<searchterm>
        Sucht im Massawiki nach Bier    
        """
        try:
            html = lxml.html.parse("http://www.massafaka.at/massawiki/doku.php?id=bier:almanach").getroot()
            result=html.cssselect('ul.toc li.level2 div.li a')        
        except: 
            irc.reply("Ich konnte das Wiki nicht öffnen.")
            return

        regex = re.compile(searchterm, re.IGNORECASE)
        name = []
        link = []
        for a in result:
            for b in regex.finditer(a.text_content()):
                name.append(a.text_content())                
                link.append(a.get('href'))

        if name: #if list is not empty, which would return 'false'
            for a,b in itertools.izip(name, link): #loop over 2 lists with itertools
                irc.reply(a, prefixNick=False)
                irc.reply('http://www.massafaka.at/massawiki/doku.php?id=bier:almanach'+b, prefixNick=False)
        else:
            irc.reply('Nichts gefunden')
        

        #resulttext=html.xpath("//ul[@class='toc']/li[@class='level2']/div[@class='li']/a/text()[contains(.,%r)]"%searchterm)
        #resultlink=html.xpath("//ul[@class='toc']/li[@class='level2']/div[@class='li']/a[text()[contains(.,%r)]]/@href"%searchterm)
        
        #for elem in result
            #irc.reply(elem.text_content())
            #irc.reply('http://www.massafaka.at/massawiki/doku.php?id=bier:almanach'+elem.get('href'))

    bwlink = wrap(bwlink, [('text')])


Class = Bierwiki


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
