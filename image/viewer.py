#if 0
# -----------------------------------------------------------------------
# iview.py - Freevo image viewer
# -----------------------------------------------------------------------
# $Id$
#
# Todo:        
#
# -----------------------------------------------------------------------
# $Log$
# Revision 1.1  2002/11/23 19:24:02  dischi
# New version of the code cleanup, not working right now, wait for more
# checkins in some minutes please
#
#
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
# -----------------------------------------------------------------------
#endif

import os.path
import Image
import signal, os, fcntl

import config # Configuration file. 
import menu   # The menu widget class
import skin   # The skin class
import osd    # The OSD class, used to communicate with the OSD daemon
import rc     # The RemoteControl class.
import exif

DEBUG = config.DEBUG

TRUE  = 1
FALSE = 0


osd        = osd.get_singleton()  # Create the OSD object
rc         = rc.get_singleton()   # Create the remote control object
menuwidget = menu.get_singleton() # Create the MenuWidget object
skin       = skin.get_singleton() # The skin object.

# Module variable that contains an initialized ImageViewer() object
_singleton = None

def get_singleton():
    global _singleton

    # One-time init
    if _singleton == None:
        _singleton = ImageViewer()
        
    return _singleton


class ImageViewer:
    osd_mode = 0    # Draw file info on the image
    zoom = 0   # Image zoom
    zoom_btns = { rc.K0:0, rc.K1:1, rc.K2:2, rc.K3:3, rc.K4:4,
                  rc.K5:5, rc.K6:6, rc.K7:7, rc.K8:8, rc.K9:9 }

    # Slide Show variables
    total_slides = 0	# Total slides in slide show
    slide_num = 0	# Current slide being displayed

    def view(self, info, zoom=0, rotation=0):
        filename = info.file
        caption = info.name

        self.fileinfo = info

        self.filename = filename
        self.caption = caption
        self.rotation = rotation

        rc.app = self.eventhandler

        width, height = osd.bitmapsize(filename)

        # Image load problem?
        if width == 0 or height == 0:
	    skin.PopupBox('Cannot load image %s!' % filename)
            return
            
        # Bounding box default values
        bbx = bby = bbw = bbh = 0

        if zoom:
            # Translate the 9-element grid to bounding boxes
            if self.rotation == 90:
                bb = { 1:(2,0), 2:(2,1), 3:(2,2),
                       4:(1,0), 5:(1,1), 6:(1,2),
                       7:(0,0), 8:(0,1), 9:(0,2) }
            elif self.rotation == 180:
                bb = { 1:(2,2), 2:(1,2), 3:(0,2),
                       4:(2,1), 5:(1,1), 6:(0,1),
                       7:(2,0), 8:(1,0), 9:(0,0) }
            elif self.rotation == 270:
                bb = { 1:(0,2), 2:(0,1), 3:(0,0),
                       4:(1,2), 5:(1,1), 6:(1,0),
                       7:(2,2), 8:(2,1), 9:(2,0) }
            else:
                bb = { 1:(0,0), 2:(1,0), 3:(2,0),
                       4:(0,1), 5:(1,1), 6:(2,1),
                       7:(0,2), 8:(1,2), 9:(2,2) }

            h, v = bb[zoom]

            # Bounding box center
            bbcx = ([1, 3, 5][h]) * width / 6
            bbcy = ([1, 3, 5][v]) * height / 6

            if self.rotation % 180:
                # different calculations because image width is screen height
                scale_x = float(osd.width) / (height / 3)
                scale_y = float(osd.height) / (width / 3)
                scale = min(scale_x, scale_y)

                # read comment for the bbw and bbh calculations below
                bbw = min(max((width / 3) * scale, osd.height), width) / scale
                bbh = min(max((height / 3) * scale, osd.width), height) / scale

            else:
                scale_x = float(osd.width) / (width / 3)
                scale_y = float(osd.height) / (height / 3)
                scale = min(scale_x, scale_y)

                # the bb width is the width / 3 * scale, to avoid black bars left
                # and right exapand it to the osd.width but not if this is more than the
                # image width (same for height)
                bbw = min(max((width / 3) * scale, osd.width), width) / scale
                bbh = min(max((height / 3) * scale, osd.height), height) / scale
                

            # calculate the beginning of the bounding box
            bbx = max(0, bbcx - bbw/2)
            bby = max(0, bbcy - bbh/2)

            if bbx + bbw > width:  bbx = width - bbw
            if bby + bbh > height: bby = height - bbh

            if self.rotation % 180:
                new_h, new_w = bbw * scale, bbh * scale
            else:
                new_w, new_h = bbw * scale, bbh * scale



        else:
            if self.rotation % 180:  
                height, width = width, height
                
            # scale_x = scale_y = 1.0
            # if width > osd.width: scale_x = float(osd.width) / width
            # if height > osd.height: scale_y = float(osd.height) / height
            scale_x = float(osd.width) / width
            scale_y = float(osd.height) / height
            
            scale = min(scale_x, scale_y)
            
            new_w, new_h = int(scale*width), int(scale*height)


        # Now we have all necessary informations about zoom yes/no and
        # the kind of rotation
        
        x = (osd.width - new_w) / 2
        y = (osd.height - new_h) / 2
        
        osd.clearscreen(color=osd.COL_BLACK)
        osd.drawbitmap(filename, x, y, scale, bbx, bby, bbw, bbh,
                       rotation = self.rotation)

        # update the OSD
        self.drawosd()

        # draw
        osd.update()


    def cache(self, fileinfo):
        # cache the next image (most likely we need this)
        osd.bitmapsize(fileinfo.file)
        
            

    def eventhandler(self, event):

        if event == rc.PAUSE:
            signal.alarm(0)

        elif event == rc.PLAY:
            signal.alarm(1)

        elif event == rc.STOP or event == rc.EXIT or event == rc.MENU:
            rc.app = None
            signal.alarm(0)
            menuwidget.refresh()

        # rotate image
        elif event == rc.LEFT or event == rc.RIGHT:
            osd.clearscreen(color=osd.COL_BLACK)

            if event == rc.RIGHT:
                self.rotation = (self.rotation + 270) % 360
            else:
                self.rotation = (self.rotation + 90) % 360


            image = Image.open(self.filename)

            if self.rotation % 180:
                height, width = image.size
            else:
                width, height = image.size

            scale_x = scale_y = 1.0
            if width > osd.width: scale_x = float(osd.width) / width
            if height > osd.height: scale_y = float(osd.height) / height

            scale = min(scale_x, scale_y)

            new_w, new_h = int(scale*width), int(scale*height)

	    self.zoom = 0

            osd.drawbitmap(self.filename, (osd.width-new_w) / 2, (osd.height-new_h) / 2,
                           scaling=scale, rotation=self.rotation)

            if self.osd_mode:
                self.drawosd()
            osd.update()

        # print image information
        elif event == rc.DISPLAY:
            self.osd_mode = {0:1, 1:2, 2:0}[self.osd_mode] # Toggle on/off
            # Redraw
            self.view(self.fileinfo, zoom=self.zoom, rotation = self.rotation)

        # zoom to one third of the image
        # 1 is upper left, 9 is lower right, 0 zoom off
        elif event in self.zoom_btns:
            self.zoom = self.zoom_btns[event]
                
            if self.zoom:
                # Zoom one third of the image, don't load the next
                # image in the list
                self.view(self.fileinfo, zoom=self.zoom, rotation = self.rotation)
            else:
                # Display entire picture, don't load next image in case
                # the user wants to zoom around some more.
                self.view(self.fileinfo, zoom=0, rotation = self.rotation)
                
        # save the image with the current rotation
        elif event == rc.REC:
            if self.rotation and os.path.splitext(self.filename)[1] == ".jpg":
                cmd = 'jpegtran -copy all -rotate %s -outfile /tmp/freevo-iview %s' \
                      % ((self.rotation + 180) % 360, self.filename)
                os.system(cmd)
                os.system('mv /tmp/freevo-iview %s' % self.filename)
                self.rotation = 0
                osd._deletefromcache(self.filename)

        else:
            self.fileinfo.eventhandler(event)
            
    def drawosd(self):

        if not self.osd_mode: return

        if self.osd_mode == 1:
            # This is where we add a caption.  Only if playlist is empty
            # May need to check the caption too?
            if self.caption:
                osd.drawstring(self.caption, 10, osd.height - 25, fgcolor=osd.COL_ORANGE, 
                               bgcolor=osd.COL_BLACK)
            return
            
        
        f = open(self.filename, 'r')
        tags = exif.process_file(f)

        # Make the background darker for the OSD info
        osd.drawbox(0, osd.height - 110, osd.width, osd.height, width=-1,
                    color=((60 << 24) | osd.COL_BLACK))
        
        pos = 50

        if tags.has_key('Image DateTime') and \
		tags.has_key('EXIF ExifImageWidth') and tags.has_key('EXIF ExifImageLength'):
            osd.drawstring('%s (%s x %s) @ %s' % \
		(os.path.basename(self.filename), 
		 tags['EXIF ExifImageWidth'], tags['EXIF ExifImageLength'], \
		 tags['Image DateTime']), \
			 20, osd.height - pos, fgcolor=osd.COL_ORANGE)
	else:
            osd.drawstring('%s' % (os.path.basename(self.filename)), \
			 20, osd.height - pos, fgcolor=osd.COL_ORANGE)

        pos += 30
            
	if tags.has_key('EXIF ExposureTime') and tags.has_key('EXIF FNumber') and \
		tags.has_key('EXIF FocalLength') and \
                tags.has_key('EXIF ISOSpeedRatings') and \
		tags.has_key('EXIF ExposureProgram') and \
                tags.has_key('EXIF MeteringMode') and \
		tags.has_key('EXIF LightSource') and tags.has_key('EXIF Flash'):
            osd.drawstring('%s sec F/%s, L=%s mm, ISO %s, %s (%s Mtr), %s (Fls %s)' % \
			 (tags['EXIF ExposureTime'], tags['EXIF FNumber'], 
			  tags['EXIF FocalLength'], tags['EXIF ISOSpeedRatings'],
			  tags['EXIF ExposureProgram'], tags['EXIF MeteringMode'], 
			  tags['EXIF LightSource'], tags['EXIF Flash']), 
			 20, osd.height - pos, fgcolor=osd.COL_ORANGE)
            pos += 30
            
        if tags.has_key('Image Make') and tags.has_key('Image Model') and \
           tags.has_key('Image Software'):
            osd.drawstring('%s %s (%s)' % (tags['Image Make'], tags['Image Model'],
                                           tags['Image Software']), 
                           20, osd.height - pos, fgcolor=osd.COL_ORANGE)
            pos += 30
            
        if self.zoom:
            osd.drawstring('Zoom = %s' % self.zoom, 20, osd.height - pos, 
                           fgcolor=osd.COL_ORANGE)
            
