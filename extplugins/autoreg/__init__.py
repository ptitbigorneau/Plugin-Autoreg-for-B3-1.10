# -*- coding: utf-8 -*-
#
# AutoReg plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.5'

import b3
import b3.plugin
import b3.events
import b3.config
from b3 import clients
from b3.functions import getCmd

class AutoregPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None

    _noclevel1 = 25
    _noclevel2 = 100

    gnamelevel0 = "Guest"
    gkeywordlevel0 = "guest"
    gnamelevel1 = "User"
    gkeywordlevel1 = "user"
    gnamelevel2 = "Regular"
    gkeywordlevel2 = "reg"
	
    def onLoadConfig(self):

        self._noclevel1 = self.getSetting('settings', 'noclevel1', b3.INT, self._noclevel1)
        self._noclevel2 = self.getSetting('settings', 'noclevel2', b3.INT, self._noclevel2)
		
    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            raise AttributeError('could not find admin plugin')

        self.registerEvent('EVT_CLIENT_AUTH', self.onClientAuth)

        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    def onClientAuth(self, event):

        client = event.client
        self.group()
            
        cgroup = client.maxGroup.name

        if (cgroup == self.gnamelevel0) and (client.connections >= self._noclevel1):
            
            test = None			

            self.debug("clientmaxLevel : %s cgroup : %s gnamelevel0 : %s"%(client.maxLevel, cgroup, self.gnamelevel0))

            try:

                group = clients.Group(keyword= self.gkeywordlevel1)
                group = self.console.storage.getGroup(group)
                
            except:
                test = "error"
                self.debug("user Group Error")
                return False
				
            if test == None:
			
                client.message('You are connected ^2%s^7 times. Thank you for your loyalty'%(client.connections))
                client.message('You are now in the group ^2%s ^7[^21^7]'%(self.gnamelevel1))                
                client.setGroup(group)
                client.save()

        if (cgroup == self.gnamelevel1) and (client.connections >= self._noclevel2):
 
            test = None

            self.debug("clientmaxLevel : %s cgroup : %s gnamelevel1 : %s"%(client.maxLevel, cgroup, self.gnamelevel1))

            try:

                group = clients.Group(keyword= self.gkeywordlevel2)
                group = self.console.storage.getGroup(group)
 
            except:
			
                test = "error"
                self.debug("regular Group Error")
                return False
				
            if test == None:
				
                client.message('You are connected ^2%s^7 times. Thank you for your loyalty'%(client.connections))
                client.message('you are now in the group ^2%s ^7[^22^7]'%(self.gnamelevel2))
                
                client.setGroup(group)
                client.save()
   
    def cmd_noc(self, data, client, cmd=None):
        
        """\
        info client connections 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!noc <name>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            if sclient.maskedGroup:
                 
                cgroup = sclient.maskedGroup.name
                
            else:
        
                cgroup = self.gnamelevel0            

            cmd.sayLoudOrPM(client, '%s^7 connected ^2%s ^7times : ^2%s^7 [^2%s^7] '%(sclient.exactName, sclient.connections, cgroup, sclient.maxLevel))  
        
        else:
            return False

    def cmd_autoreg(self, data, client, cmd=None):
        
        """\
        activate / deactivate autoreg or change number of connections
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:

            cmd.sayLoudOrPM(client, 'The number of connections for ^3Level1 ^7is ^2%s^7 '%(self._noclevel1))
            cmd.sayLoudOrPM(client, 'The number of connections for ^3Level2 ^7is ^2%s^7 '%(self._noclevel2))
            cmd.sayLoudOrPM(client, '!autoreg <level1 or level2> <number of connections>')
            
            return False
    
        if input[0] == 'level1' or input[0] == 'level2':

                if input[1]:

                    if input[1].isdigit():
                        
                        if input[0] == 'level1':
                            self._noclevel1 = input[1]
                            settingname = 'noclevel1'

                        if input[0] == 'level2':
                            self._noclevel2 = input[1]
                            settingname = 'noclevel2'

                        settingsvalue = input[1]
                        message = 'The number of connections for ^3%s ^7is now ^2%s^7 '%(input[0], settingsvalue)

                    else:

                        cmd.sayLoudOrPM(client, '!autoreg <level1 or level2> <number of connections>')

                        return False

                else:

                    if input[0] == 'level1':
                        cmd.sayLoudOrPM(client, 'The number of connections for ^3%s ^7is ^2%s^7 '%(input[0], self._noclevel1))
                                            
                    if input[0] == 'level2':
                        cmd.sayLoudOrPM(client, 'The number of connections for ^3%s ^7is ^2%s^7 '%(input[0], self._noclevel2))
                    
                    cmd.sayLoudOrPM(client, '!autoreg <level1 or level2> <number of connections>')

                    return False

        else:
		
            cmd.sayLoudOrPM(client, '!autoreg <on / off> or <level1 or level2> <number of connections>')

            return False

        client.message('%s '%(message))

        modif = "%s: %s\n"%(settingname, settingsvalue)

        fichier = self.config.fileName

        autoregini = open(fichier, "r")
        
        contenu = autoregini.readlines()

        autoregini.close()

        newcontenu = ""

        for ligne in contenu:

            if settingname in ligne:

                ligne = modif

            newcontenu = "%s%s"%(newcontenu, ligne)        

        autoreginiw = open(fichier, "w")
        autoreginiw.write(newcontenu)
        autoreginiw.close()

    def group(self):

        self.rgname = None
        self.rgkeyword = None
    
        cursor = self.console.storage.query("""
        SELECT *
        FROM groups n 
        """)

        if cursor.EOF:
  
            cursor.close()            
            
            return False

        while not cursor.EOF:
        
            sr = cursor.getRow()
            gname= sr['name']
            gkeyword = sr['keyword']
            glevel= sr['level']
       
            if glevel == 0:

                self.gnamelevel0 = gname
                self.gkeywordlevel0 = gkeyword

            if glevel == 1:

                self.gnamelevel1 = gname
                self.gkeywordlevel1 = gkeyword

            if glevel == 2:

                self.gnamelevel2 = gname
                self.gkeywordlevel2 = gkeyword

            cursor.moveNext()
    
        cursor.close()

        return
