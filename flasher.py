#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
S3C 6410 Flash main UI code
Author: Amankwah <amankwah7@gmail.com>
License: GPLv2
'''

import pygtk
pygtk.require('2.0')
import gtk, gobject

import os, re

def get_sd_devices(combox=None):
    if combox is None:
        return False
    if type(combox) is not gtk.ComboBox:
        return False
    dev_li=[]
    ch_li=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    try:
        for ch in ch_li:
            f=file("/sys/block/sd%s/removable" %(ch), "r")
            b=f.read()
            if b == '0\n':
                pass
                # print "/dev/sd%s is fixed." %(ch)
            else:
                # print "/dev/sd%s is removable." %(ch)
                combox.append_text("/dev/sd%s" %(ch))
    except Exception, ex:
        pass
        # print ex
    combox.set_active(0)
    return dev_li

def get_macro_value_in_c_header(s=None, d=None):
    rp=r'^\#\s*define\s+' + s + r'\s+.*'
    return re.compile(r'(?<=\()0x[abcdef\d]+|0[01234567]*|\d+', re.I).\
        findall(re.compile(rp, re.M).findall(d)[0])[0]

class mw:
    def on_window_main_delete_event(self, widget, data=None):
        gtk.main_quit()

    def on_button_flash_clicked(self, button, data=None):
        is_sdhc	= 0
        if self.ckb_sdhc.get_active():
            is_sdhc	= 1
        cardname	= self.combobox_card.get_active_text()

        if self.checkbutton2.get_active():
            os.system('dd if="%s" of="%s" bs=512 seek=%i'
                      %(self.filechooserbutton1.get_filename(),
                        cardname,
                        self.blocks - 16 - 1 - 1 - 1024 * is_sdhc))
        if self.checkbutton3.get_active():
            os.system('dd if="%s" of="%s" bs=512 seek=%i'
                      %(self.filechooserbutton2.get_filename(),
                        cardname,
                        self.blocks - int(self.entry1.get_text(), 0) / 512 - 1024 * is_sdhc))
        if self.checkbutton4.get_active():
            os.system('dd if="%s" of="%s" bs=512 seek=%i'
                      %(self.filechooserbutton3.get_filename(),
                        cardname,
                        self.blocks - int(self.entry2.get_text(), 0) / 512 - 1024 * is_sdhc))
        if self.checkbutton_bksz.get_active():
            os.system('dd if="%s" of="%s" bs=512 seek=%i'
                      %(self.filechooserbutton4.get_filename(),
                        cardname,
                        self.blocks - int(self.entry3.get_text(), 0) / 512 - 1024 * is_sdhc))

    def on_button_erase_clicked(self, button, data=None):
        print button, data

    def on_filechooserbutton_ubsrc_file_set(self, fc_button, data=None):
        self.ubsrc_path	= fc_button.get_filename()
        fpath	= "%s/include/configs/mini6410.h" %(self.ubsrc_path)
        if os.path.isfile(fpath):
            self.fc_button_header.select_filename(fpath)
            li=open(fpath, 'r').read()
            self.entry1.set_text(get_macro_value_in_c_header('MMC_UBOOT_POS_BACKWARD', li))
            self.entry2.set_text(get_macro_value_in_c_header('MMC_ENV_POS_BACKWARD', li))
            self.entry3.set_text(get_macro_value_in_c_header('MMC_BACKGROUND_POS_BACKWARD', li))
        # FIXME: add a warning box when the file is not exist.

        fpath	= "%s/u-boot.bin" %(self.ubsrc_path)
        if os.path.isfile(fpath):
            self.filechooserbutton2.select_filename(fpath)
            self.checkbutton3.set_label("Size:%u" %(os.path.getsize(fpath)))
            self.checkbutton3.set_active(True)

        fpath	= "%s/nand_spl/u-boot-spl-16k.bin" %(self.ubsrc_path)
        if os.path.isfile(fpath):
            self.filechooserbutton1.select_filename(fpath)
            self.checkbutton2.set_label("Size:%u" %(os.path.getsize(fpath)))
            self.checkbutton2.set_active(True)

    def on_filechooserbutton_header_file_set(self, fc_button, data=None):
        self.header_filename	= fc_button.get_filename()
        # self.fc_button_ubsrc.select_filename(os.path.dirname(self.header_filename))
        li=open(self.header_filename, 'r').read()
        self.entry1.set_text(get_macro_value_in_c_header('MMC_UBOOT_POS_BACKWARD', li))
        self.entry2.set_text(get_macro_value_in_c_header('MMC_ENV_POS_BACKWARD', li))
        self.entry3.set_text(get_macro_value_in_c_header('MMC_BACKGROUND_POS_BACKWARD', li))

    def on_filechooserbutton_bk_bmp_file_set(self, fc_button, data=None):
        f_name	= fc_button.get_filename()
        fk, fx, fy	= gtk.gdk.pixbuf_get_file_info(f_name)
        dx, dy		= self.hbox2.size_request()
        dx	       	= dx / 2
        x, y		= (dx, dy)
        if dx / dy > fx / fy:
            x	= int(dy * (float(fx) / fy))
        else:
            y	= int(dx * (float(fy) / fx))
        pb	= gtk.gdk.pixbuf_new_from_file_at_size(f_name, x, y)
        self.image_bk_bmp.set_from_pixbuf(pb)
        self.checkbutton_bksz.set_label("Size:%u" %(os.path.getsize(f_name)))
        self.checkbutton_bksz.set_active(True)

    def on_drawingarea_bar_expose_event(self, drawingarea, event):
        print "Draw the picture will implement in future."

    def on_ckb_sdhc_toggled(self, t_button, data=None):
        if gtk.ToggleButton.get_active(t_button):
            self.image_sd.set_from_file("./sdhc.png")
        else:
            self.image_sd.set_from_file("./sd.png")

    def on_liststore2_row_changed(self, model=None, tpath=None, it=None):
        dev_name	= os.path.basename(model.get_value(it, 0))
        bsizefile	= open("/sys/block/%s/size" %(dev_name), "r")
        bsize		= bsizefile.readline()
        bsizefile.close()
        self.button_flash.set_sensitive(True)
        self.button_erase.set_sensitive(True)
        self.lbl_total_block.set_text("Total block: %s" %(bsize))
        self.blocks	= int(bsize, 0)
        if self.blocks > (1024 * 1024 * 1024 * 2 / 512):
            self.ckb_sdhc.set_active(True)
        else:
            self.ckb_sdhc.set_active(False)

    def on_combobox_card_changed(self, cbox):
        idx	= cbox.get_active()
        if idx > -1:
            it	= self.liststore2.get_iter("%i" %(idx))
            self.on_liststore2_row_changed(self.liststore2, None, it)

    def on_filechooserbutton1_file_set(self, button, data=None):
        f_name	= button.get_filename()
        self.checkbutton2.set_label("Size:%u" %(os.path.getsize(f_name)))
        self.checkbutton2.set_active(True)

    def on_filechooserbutton2_file_set(self, button, data=None):
        f_name	= button.get_filename()
        self.checkbutton3.set_label("Size:%u" %(os.path.getsize(f_name)))
        self.checkbutton3.set_active(True)

    def on_filechooserbutton3_file_set(self, button, data=None):
        f_name	= button.get_filename()
        self.checkbutton4.set_label("Size:%u" %(os.path.getsize(f_name)))
        self.checkbutton4.set_active(True)

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
        self.lbl_total_block	= builder.get_object('lbl_total_block')
        self.ckb_sdhc		= builder.get_object('ckb_sdhc')
        self.liststore2		= builder.get_object('liststore2')
        self.entry1		= builder.get_object('entry1')
        self.entry2		= builder.get_object('entry2')
        self.entry3		= builder.get_object('entry3')
        self.checkbutton2	= builder.get_object('checkbutton2')
        self.checkbutton3	= builder.get_object('checkbutton3')
        self.checkbutton4	= builder.get_object('checkbutton4')
        self.hbox2		= builder.get_object('hbox2')
        self.button_flash	= builder.get_object('button_flash')
        self.button_erase	= builder.get_object('button_erase')
        self.filechooserbutton1	= builder.get_object('filechooserbutton1')
        self.filechooserbutton2	= builder.get_object('filechooserbutton2')
        self.filechooserbutton3	= builder.get_object('filechooserbutton3')
        self.filechooserbutton4 = builder.get_object('filechooserbutton_bk_bmp')
        builder.connect_signals(self)
        get_sd_devices(self.combobox_card)
        self.window_main.show()
        


if __name__=="__main__":
    app	= mw()
    gtk.main()
