#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''S3C 6410 Flash main UI code
'''
import pygtk
pygtk.require('2.0')
import gtk


class mw:
    def on_window_main_delete_event(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        builder	=gtk.Builder()
        builder.add_from_file('./flasher.glade')
        self.window_main	= builder.get_object('window_main')
        builder.connect_signals(self)
        self.window_main.show()


if __name__=="__main__":
    app	= mw()
    gtk.main()
