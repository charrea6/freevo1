# -*- coding: iso-8859-1 -*-
# -----------------------------------------------------------------------
# Audio DetachBar plug-in
# -----------------------------------------------------------------------
# $Id$
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
# -----------------------------------------------------------------------


"""
Audio DetachBar plug-in

Author: Viggo Fredriksen <viggo@katatonic.org>
"""

# python specific
import time
import rc

# freevo specific
import config
import skin
import audio.player
import plugin
from event import *


# barstates
BAR_HIDE=0              # timedout, reset and change poll interval
BAR_SHOW=1              # show the bar
BAR_IDLE=2              # wait for new track

class PluginInterface(plugin.DaemonPlugin):
    """
    This plugin enables a small bar showing information about audio being played
    when detached with the detach plugin.

    If the idlebar is loaded and there is enough space left there, this plugin
    will draw itself there, otherwise it will draw at the right bottom of the
    screen.
    """

    def __init__(self):
        """initialise the DaemonPlugin interface"""
        _debug_('detachbar.PluginInterface.__init__(self)', 2)
        plugin.DaemonPlugin.__init__(self)
        self.plugin_name = 'audio.detachbar'
        self.update_registered = False
        # tunables
        self.TimeOut  = 3  # 3 seconds till we hide the bar
        self.hide()


    def timer(self):
        """
        internal timer
        returns status based on idletime
        """
        _debug_('timer(self)', 3)
        if self.Timer:
            diff = time.time() - self.Timer
            if diff > self.TimeOut:
                return BAR_HIDE
            else:
                return BAR_IDLE


    def eventhandler(self, event, menuw=None):
        """
        Needed to catch the plugin DETACH event
        """
        _debug_('eventhandler(self, event, menuw=None)', 2)
        if plugin.isevent(event) == 'DETACH':
            self.show()
            return True
        return False


    def hide(self):
        """
        used when hiding the bar
        """
        _debug_('hide(self)', 2)
        self.status = BAR_HIDE
        self.render = []
        self.player = None
        self.Timer  = None
        self.bar    = None
        if self.update_registered:
            rc.unregister(self.update)
            self.update_registered = False


    def show(self):
        """
        used when showing for the first time
        """
        _debug_('show(self)', 2)
        self.player = audio.player.get()
        if not self.update_registered:
            rc.register(self.update, True, 10)
            self.update_registered = True
        self.getInfo()
        self.status = BAR_SHOW


    def stop(self):
        """
        stops the player, waiting for timeout
        """
        _debug_('stop(self)', 2)
        self.status = BAR_IDLE
        self.Timer  = time.time()


    def update(self):
        """
        update the bar according to showstatus
        """
        _debug_('update(self)', 3)
        if self.status == BAR_SHOW:
            if skin.active():
                skin.redraw()

        elif self.status == BAR_IDLE:
            self.status = self.timer()
            if self.status == BAR_HIDE:
                self.hide()
            if skin.active():
                skin.redraw()


    def draw(self, (type, object), osd):
        """
        draws the bar
        """
        _debug_('draw(self, (type, object), osd)', 3)
        if self.status == BAR_IDLE:
            # when idle, wait for a new player
            if audio.player.get():
                self.show()

        if self.status == BAR_SHOW:
            if not self.player.running:
                # player stopped, we also stop
                # and wait for a new one
                self.player = None
                self.stop()
                return

            if type == 'player':
                # Oops, showing the player again, stop me
                self.stop()
                self.hide()
                return

            font = osd.get_font('detachbar')

            if font == osd.get_font('default'):
                font = osd.get_font('info value')

            self.calculatesizes(osd, font)

            if self.image:
                x = self.x - self.h
                width  = self.w + 70 - 10
            else:
                x = self.x
                width = self.w

            if not self.idlebar:
                y = self.y - 10
                height = self.h
                osd.drawroundbox(x, y, width, height, (0xf0ffffffL, 5, 0xb0000000L, 10))

            if self.image:
                osd.draw_image(self.image, (x+5, self.y, 50, 50))

            y = self.t_y

            for r in self.render:
                osd.write_text(r, font, None, self.t_x, y, self.t_w, self.font_h, 'center', 'center')
                y += self.font_h

            if self.player.item.length:
                progress = '%s/%s' % (self.formattime(self.player.item.elapsed),
                    self.formattime(self.player.item.length))
            else:
                progress = '%s' % self.formattime(self.player.item.elapsed)

            osd.write_text(progress, font, None, self.t_x, y, self.t_w, self.font_h, 'center', 'center')
        return 0


    def getInfo(self):
        """
        sets an array of things to draw
        """
        _debug_('getInfo(self)', 2)
        self.render = []
        self.calculate = True
        info = self.player.item.info

        self.image =  self.player.item.image
        # artist : album
        if info['artist'] and info['album']:
            self.render += [ '%s : %s' % (info['artist'], info['album']) ]
        elif info['album']:
            self.render += [ info['album'] ]
        elif info['artist']:
            self.render += [ info['artist'] ]

        # trackno - title
        if info['trackno'] and info['title']:
            self.render += [ '%s - %s' % (info['trackno'], info['title'] ) ]
        elif info['title']:
            self.render += [ info['title'] ]

        # no info available
        if len(self.render)==0:
            self.render += [ self.player.item.name ]


    def calculatesizes(self, osd, font):
        """
        sizecalcs is not necessery on every pass
        """
        _debug_('calculatesizes(osd, font)', 3)
        if not hasattr(self, 'idlebar'):
            self.idlebar = plugin.getbyname('idlebar')
            if self.idlebar:
                self.idlebar_max = osd.width + osd.x
                for p in plugin.get('idlebar'):
                    if hasattr(p, 'clock_left_position'):
                        self.idlebar_max = p.clock_left_position

                if self.idlebar_max - self.idlebar.free_space < 250:
                    _debug_('free space in idlebar to small, using normal detach')
                    self.idlebar = None


        pad_internal = 5 # internal padding for box vs text

        if self.calculate:
            self.calculate = False
            self.font_h = font.font.height

            total_width = osd.width + 2*osd.x
            total_height = osd.height + 2*osd.y
            pad = 10 # padding for safety (overscan may not be 100% correct)
            bar_height = self.font_h
            bar_width = 0

            for r in self.render:
                bar_height += self.font_h
                bar_width = max(bar_width, font.font.stringsize(r))

            y = total_height - bar_height - config.OSD_OVERSCAN_BOTTOM - skin.attr_global_dict['buttonbar_height']
            x = total_width - bar_width - config.OSD_OVERSCAN_RIGHT
            self.y = y - osd.y - pad - pad_internal
            self.x = x - osd.x - pad - pad_internal
            self.w = bar_width + pad + pad_internal + 10
            self.h = 70
            self.t_y = self.y + pad_internal
            self.t_x = self.x + pad_internal
            self.t_w = bar_width + 5 # in case of shadow

        if self.idlebar:
            self.y = osd.y + 5
            self.x = self.image and self.idlebar.free_space + 70 or self.idlebar.free_space
            self.t_y = self.y
            self.t_x = self.x
            self.t_w = min(self.t_w, self.idlebar_max - self.x - 30)


    def formattime(self, seconds):
        """
        returns string formatted as mins:seconds
        """
        _debug_('formattime(self, seconds)', 3)
        mins = 0
        mins = seconds / 60
        secs = seconds % 60

        if secs<10:
            secs = '0%s' % secs
        else:
            secs = '%s' % secs
        return '%i:%s' % (mins, secs)
