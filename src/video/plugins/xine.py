#if 0 /*
# -----------------------------------------------------------------------
# xine.py - the Freevo XINE module for video
# -----------------------------------------------------------------------
# $Id$
#
# Notes:
#
# Activate this plugin by putting plugin.activate('video.xine') in your
# local_conf.py. Than xine will be used for DVDs when you SELECT the item.
# When you select a title directly in the menu, this plugin won't be used
# and the default player (mplayer) will be used. You need xine-ui >= 0.9.22
# to use this.
#
# Todo:        
#
#
# -----------------------------------------------------------------------
# $Log$
# Revision 1.32  2003/12/10 19:47:49  dischi
# make it possible to bypass version checking
#
# Revision 1.31  2003/12/10 19:06:06  dischi
# move to new ChildApp2 and remove the internal thread
#
# Revision 1.30  2003/12/07 08:57:20  dischi
# add config.XINE_ARGS_DEF
#
# Revision 1.29  2003/12/07 08:32:14  dischi
# make keybindings work for files and urls
#
# Revision 1.28  2003/12/06 16:25:45  dischi
# support for type=url and <playlist> and <player>
#
# Revision 1.27  2003/11/30 19:41:57  dischi
# enhance interlacing, needs xine cvs to work as it should
#
# Revision 1.26  2003/11/29 18:37:30  dischi
# build config.VIDEO_SUFFIX in config on startup
#
# Revision 1.25  2003/11/28 20:08:59  dischi
# renamed some config variables
#
# Revision 1.24  2003/11/28 19:26:37  dischi
# renamed some config variables
#
# Revision 1.23  2003/11/22 21:23:55  dischi
# fix dvd title playing
#
# Revision 1.22  2003/11/22 15:57:47  dischi
# cleanup
#
# Revision 1.21  2003/11/21 17:56:50  dischi
# Plugins now 'rate' if and how good they can play an item. Based on that
# a good player will be choosen.
#
# Revision 1.20  2003/11/09 12:01:00  dischi
# add subtitle selection and osd info support for xine (needs current xine-ui cvs
#
# -----------------------------------------------------------------------
# Freevo - A Home Theater PC framework
# Copyright (C) 2002 Krister Lagerstrom, et al. 
# Please see the file freevo/Docs/CREDITS for a complete list of authors.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MER-
# CHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# ----------------------------------------------------------------------- */
#endif


import time, os, re
import copy

import config     # Configuration handler. reads config file.
import childapp   # Handle child applications
import rc         # The RemoteControl class.
import util.popen3

from event import *
import plugin


class PluginInterface(plugin.Plugin):
    """
    Xine plugin for the video player.
    """
    def __init__(self):
        plugin.Plugin.__init__(self)

        try:
            config.XINE_COMMAND
        except:
            print _( 'ERROR' ) + ': ' + \
                  _("'XINE_COMMAND' not defined, plugin 'xine' deactivated")
            print _( 'please check the xine section in freevo_config.py' )
            return

        if config.XINE_COMMAND.find('fbxine') >= 0:
            type = 'fb'
        else:
            type = 'X'

        if not hasattr(config, 'XINE_VERSION'):
            config.XINE_VERSION = 0
            for data in util.popen3.stdout('%s --version' % config.XINE_COMMAND):
                m = re.match('^.* v?([0-9])\.([0-9]+)\.([0-9]*).*', data)
                if m:
                    config.XINE_VERSION = int('%02d%02d%02d' % (int(m.group(1)),
                                                                  int(m.group(2)),
                                                                  int(m.group(3))))
                    if data.find('cvs') >= 0:
                        config.XINE_VERSION += 1

            _debug_('detect xine version %s' % config.XINE_VERSION)
            
        if config.XINE_VERSION < 922:
            if type == 'fb':
                print _( 'ERROR' ) + ': ' + \
                      _( "'fbxine' version too old, plugin 'xine' deactivated" )
                print _( 'You need software %s' ) % 'xine-ui > 0.9.21'
                return
            print _( 'WARNING' ) + ': ' + \
                  _( "'xine' version too old, plugin in fallback mode" )
            print _( "You need %s to use all features of the '%s' plugin" ) % \
                  ( 'xine-ui > 0.9.21', 'xine' )
            
        # register xine as the object to play
        plugin.register(Xine(type, config.XINE_VERSION), plugin.VIDEO_PLAYER, True)


class Xine:
    """
    the main class to control xine
    """
    
    def __init__(self, type, version):
        self.name = 'xine'

        self.mode         = None
        self.app_mode     = ''
        self.xine_type    = type
        self.xine_version = version
        self.app          = None

        self.command = [ '--prio=%s' % config.MPLAYER_NICE ] + \
                       config.XINE_COMMAND.split(' ') + \
                       [ '--stdctl', '-V', config.XINE_VO_DEV, '-A', config.XINE_AO_DEV ] +\
                       config.XINE_ARGS_DEF.split(' ')


    def rate(self, item):
        """
        How good can this player play the file:
        2 = good
        1 = possible, but not good
        0 = unplayable
        """
        if item.mode == 'dvd':
            return 2
        if item.mode == 'vcd':
            if self.xine_version > 922:
                if not item.filename or item.filename == '0':
                    return 2
                return 0
            else:
                return 0
        if os.path.splitext(item.filename)[1][1:].lower() in \
               config.VIDEO_XINE_SUFFIX:
            return 2
        if item.mode == 'url':
            return 1
        return 0
    
    
    def play(self, options, item):
        """
        play a dvd with xine
        """
        self.item     = item
        self.app_mode = item.mode
        if item.mode in ('file', 'url'):
             self.app_mode = 'video'

        if plugin.getbyname('MIXER'):
            plugin.getbyname('MIXER').reset()

        command = copy.copy(self.command)

        if item.deinterlace and (self.xine_type == 'X' or self.xine_version > 922):
            command.append('-D')

        if not rc.PYLIRC and '--no-lirc' in command:
            command.remove('--no-lirc')

        if self.xine_version < 922:
            for arg in command:
                if arg.startswith('--post'):
                    command.remove(arg)
                    break
                
        self.max_audio        = 0
        self.current_audio    = -1
        self.max_subtitle     = 0
        self.current_subtitle = -1

        if item.mode == 'dvd' and item.url == 'dvd://':
            for track in item.info['tracks']:
                self.max_audio = max(self.max_audio, len(track['audio']))

            for track in item.info['tracks']:
                self.max_subtitle = max(self.max_subtitle, len(track['subtitles']))

        if item.mode == 'dvd':
            # dvd:///dev/dvd/2
            if not item.filename or item.filename == '0':
                track = ''
            else:
                track = item.filename
            command.append('dvd://%s/%s' % (item.media.devicename, track))

        elif item.mode == 'vcd':
            # vcd:///dev/cdrom -- NO track support (?)
            command.append('vcd://%s' % item.media.devicename)

        elif item.mime_type == 'cue':
            command.append('vcd://%s' % item.filename)
            self.app_mode = 'vcd'
            
        else:
            command.append(item.url)
            
        _debug_('Xine.play(): Starting cmd=%s' % command)

        rc.app(self)
        self.app = childapp.ChildApp2(command)
        return None
    

    def stop(self):
        """
        Stop xine
        """
        self.app.stop('quit\n')
        rc.app(None)
            

    def eventhandler(self, event, menuw=None):
        """
        eventhandler for xine control. If an event is not bound in this
        function it will be passed over to the items eventhandler
        """
        if event in ( PLAY_END, USER_END ):
            self.stop()
            return self.item.eventhandler(event)

        # fallback for older versions of xine
        if self.xine_version < 922:
            return True
        
        if event == PAUSE or event == PLAY:
            self.app.write('pause\n')
            return True

        if event == STOP:
            self.stop()
            return self.item.eventhandler(event)

        if event == SEEK:
            pos = int(event.arg)
            if pos < 0:
                action='SeekRelative-'
                pos = 0 - pos
            else:
                action='SeekRelative+'
            if pos <= 15:
                pos = 15
            elif pos <= 30:
                pos = 30
            else:
                pos = 30
            self.app.write('%s%s\n' % (action, pos))
            return True

        if event == TOGGLE_OSD:
            self.app.write('OSDStreamInfos\n')
            return True

        if event == VIDEO_TOGGLE_INTERLACE:
            self.app.write('ToggleInterleave\n')
            return True

        if event == NEXT:
            self.app.write('EventNext\n')
            return True

        if event == PREV:
            self.app.write('EventPrior\n')
            return True

        # DVD NAVIGATION
        if event == DVDNAV_LEFT:
            self.app.write('EventLeft\n')
            return True
            
        if event == DVDNAV_RIGHT:
            self.app.write('EventRight\n')
            return True
            
        if event == DVDNAV_UP:
            self.app.write('EventUp\n')
            return True
            
        if event == DVDNAV_DOWN:
            self.app.write('EventDown\n')
            return True
            
        if event == DVDNAV_SELECT:
            self.app.write('EventSelect\n')
            return True
            
        if event == DVDNAV_TITLEMENU:
            self.app.write('TitleMenu\n')
            return True
            
        if event == DVDNAV_MENU:
            self.app.write('Menu\n')
            return True

        # VCD NAVIGATION
        if event in INPUT_ALL_NUMBERS:
            self.app.write('Number%s\n' % event.arg)
            time.sleep(0.1)
            self.app.write('EventSelect\n')
            return True
        
        if event == MENU:
            self.app.write('TitleMenu\n')
            return True


        # DVD/VCD language settings
        if event == VIDEO_NEXT_AUDIOLANG and self.max_audio:
            if self.current_audio < self.max_audio - 1:
                self.app.write('AudioChannelNext\n')
                self.current_audio += 1
                # wait until the stream is changed
                time.sleep(0.1)
            else:
                # bad hack to warp around
                if self.xine_type == 'fb':
                    self.app.write('AudioChannelDefault\n')
                    time.sleep(0.1)
                for i in range(self.max_audio):
                    self.app.write('AudioChannelPrior\n')
                    time.sleep(0.1)
                self.current_audio = -1
            return True
            
        if event == VIDEO_NEXT_SUBTITLE and self.max_subtitle:
            if self.current_subtitle < self.max_subtitle - 1:
                self.app.write('SpuNext\n')
                self.current_subtitle += 1
                # wait until the stream is changed
                time.sleep(0.1)
            else:
                # bad hack to warp around
                if self.xine_type == 'fb':
                    self.app.write('SpuDefault\n')
                    time.sleep(0.1)
                for i in range(self.max_subtitle):
                    self.app.write('SpuPrior\n')
                    time.sleep(0.1)
                self.current_subtitle = -1
            return True
            
        # nothing found? Try the eventhandler of the object who called us
        return self.item.eventhandler(event)
