#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''S3C 6410 Flash main UI code
'''
import pygtk
pygtk.require('2.0')
import gtk

import os


class mw:
    def on_window_main_delete_event(self, widget, data=None):
        gtk.main_quit()

    def on_button_flash_clicked(self, button, data=None):
        print button, data

    def on_button_erase_clicked(self, button, data=None):
        print button, data

    def on_filechooserbutton_ubsrc_file_set(self, fc_button, data=None):
        self.ubsrc_path	= fc_button.get_filename()
        self.fc_button_header.select_filename("%s/mini6410.h" %(self.ubsrc_path))

    def on_filechooserbutton_header_file_set(self, fc_button, data=None):
        self.header_filename	= fc_button.get_filename()
        self.fc_button_ubsrc.select_filename(os.path.dirname(self.header_filename))

    def on_filechooserbutton_bk_bmp_file_set(self, fc_button, data=None):
        f_name	= fc_button.get_filename()
        self.image_bk_bmp.set_from_file(f_name)
        self.checkbutton_bksz.set_label("Size:%u" %(os.path.getsize(f_name)))

    def on_drawingarea_bar_expose_event(self, drawingarea, event):
        print self, drawingarea, event

    def __init__(self):
        builder	= gtk.Builder()
        builder.add_from_file('./flasher.glade')
        self.window_main	= builder.get_object('window_main')
        self.combobox_card	= builder.get_object('combobox_card')
        self.fc_button_ubsrc	= builder.get_object('filechooserbutton_ubsrc')
        self.fc_button_header	= builder.get_object('filechooserbutton_header')
        self.image_sd		= builder.get_object('image_sd')
        self.image_bk_bmp	= builder.get_object('image_bk_bmp')
        self.checkbutton_bksz	= builder.get_object('checkbutton_bksz')
        builder.connect_signals(self)
        self.window_main.show()


if __name__=="__main__":
    app	= mw()
    gtk.main()
