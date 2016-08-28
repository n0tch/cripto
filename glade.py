#!/usr/bin/python
# coding: utf-8

from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import os
import hashlib
import base64

class Glade(Gtk.Window):
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file(os.getcwd() + "/janela2.glade")
		window = builder.get_object("window1")
		window.set_title("Criptografador")

		#objetos de entrada/saida de dados
		self.entry = builder.get_object("edtEntrada")
		self.buffer = builder.get_object("textbuffer")
		self.radioCript = builder.get_object("radioCript")
		self.radioDecript = builder.get_object("radioDecript")
		self.image1 = builder.get_object("image1")
		self.image2 = builder.get_object("image2")
		self.lblWelcome = builder.get_object("lblWelcome")
		self.lblTxt = builder.get_object("lblTxt")
		self.btnGo = builder.get_object("btnGo")
		self.btnLimpar = builder.get_object("btnLimpar")
		self.btnCopy = builder.get_object("btnCopy")
		self.textview = builder.get_object("textview")

		self.list_tipo = builder.get_object("list_tipo")


		#configuracao da combobox
		self.combo = builder.get_object("combobox")
		self.combo.new_with_model(self.list_tipo)
		renderer_text = Gtk.CellRendererText()
		self.combo.pack_start(renderer_text, True)
		self.combo.add_attribute(renderer_text, "text", 0)

		self.lblWelcome.set_name("wellcome")
		self.lblTxt.set_name("commonText")
		self.btnGo.set_name("btnGo")
		self.btnLimpar.set_name("btnLimpar")
		self.btnCopy.set_name("btnCopy")
		self.entry.set_name("entry")
		self.combo.set_name("combo")
		self.textview.set_name("textview")
		
		#objeto para ctrl + c
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

		self.modos = [	["MD5", 0,0],
						["SHA1", 1,0],
						["SHA224", 2,0],
						["SHA256", 3,0],
						["SHA384", 4,0],
						["SHA512", 5,0],
						["BASE16", 6,1],
						["BASE32", 7,1],
						["BASE64", 8,1]]

		#configuracao da lista de tipos de criptografia

		for modo in self.modos:
			self.list_tipo.append([str(modo[0]), int(modo[1])])

		self.combo.set_active(0)

		self.tipo = ("SHA224", 0) #coloco o primeiro item como default na combobox

		self.pb = Pixbuf.new_from_file_at_size('img/python.png', 155, 112)
		self.image1.set_from_pixbuf(self.pb)

		self.entry.connect("activate", self.criptografrar)

		builder.connect_signals({
			"on_combobox_changed":self.get_type,
			"on_btnGo_clicked":self.criptografrar,
			"on_btnCopy_clicked":self.copyText,
			"on_btnLimpar_clicked":self.limpar,
			"on_radioCript_toggled":self.changeListCript,
			"on_radioDecript_toggled":self.changeListDecript
			})

		self.gtkStyle()

		window.show()
		window.connect("delete-event", Gtk.main_quit)

	def gtkStyle(self):
		css = '''
				@import url("css/style.css");

				GtkWindow{
				    background-color: #111111;
				}

			'''
		self.stylecssprovider = Gtk.CssProvider()
		self.stylecssprovider.load_from_data(css)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.stylecssprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	def get_type(self, widget):
		tree_iter = widget.get_active_iter()
		if tree_iter != None:
			model = widget.get_model()
			name, row_id = model[tree_iter][:2]
			self.tipo = (name, row_id)
		else:
			pass

	def criptografrar(self, widget):

		def criptMD5(text):
			return hashlib.md5(text).hexdigest()

		def criptSSH1(text):
			return hashlib.sha1(text).hexdigest()

		def criptSSH224(text):
			return hashlib.sha224(text).hexdigest()

		def criptSSH256(text):
			return hashlib.sha256(text).hexdigest()

		def criptSSH384(text):
			return hashlib.sha384(text).hexdigest()

		def criptSSH512(text):
			return hashlib.sha512(text).hexdigest()

		def criptBase16(text):
			return base64.b16encode(text)

		def criptBase32(text):
			return base64.b32encode(text)

		def criptBase64(text):
			return base64.b64encode(text)

		def decriptBase16(text):
			try:
				return base64.b16decode(text)
			except:
				return "Hash não encontrado."

		def decriptBase32(text):
			try:
				return base64.b32decode(text)
			except:
				return "Hash não encontrado."

		def decriptBase64(text):
			try:
				return base64.b64decode(text)
			except:
				return "Hash não encontrado."


		text = ""
		if self.entry.get_text():
			if self.radioCript.get_active():
				if self.tipo[1] == 0:
					text = criptMD5(str(self.entry.get_text()))
				elif self.tipo[1] == 1:
					text = criptSSH1(str(self.entry.get_text()))
				elif self.tipo[1] == 2:
					text = criptSSH224(str(self.entry.get_text()))
				elif self.tipo[1] == 3: 
					text = criptSSH256(str(self.entry.get_text()))
				elif self.tipo[1] == 4:
					text = criptSSH384(str(self.entry.get_text()))
				elif self.tipo[1] == 5:
					text = criptSSH512(str(self.entry.get_text()))
				elif self.tipo[1] == 6:
					text = criptBase16(str(self.entry.get_text()))
				elif self.tipo[1] == 7:
					text = criptBase32(str(self.entry.get_text()))
				elif self.tipo[1] == 8:
					text = criptBase64(str(self.entry.get_text()))
			else:
				if self.tipo[1] == 6:
					text = decriptBase16(str(self.entry.get_text()))
				elif self.tipo[1] == 7:
					text = decriptBase32(str(self.entry.get_text()))
				elif self.tipo[1] == 8:
					text = decriptBase64(str(self.entry.get_text()))

			self.buffer.set_text(text)
		else:
			self.entry.grab_focus()

	def copyText(self, widget):
		if self.buffer.get_text(self.buffer.get_start_iter(),self.buffer.get_end_iter(),True):
			self.clipboard.set_text(
							self.buffer.get_text(self.buffer.get_start_iter(),
												 self.buffer.get_end_iter(),
												  True),
												-1)

	def limpar(self, widget):
		self.entry.set_text("")
		self.buffer.set_text("")
		self.combo.set_active(0)

	def changeListCript(self, widget):
		self.list_tipo.clear()

		for modo in self.modos:
			self.list_tipo.append([str(modo[0]), int(modo[1])])

		self.combo.set_active(0)

	def changeListDecript(self, widget):
		self.list_tipo.clear()
		for modo in self.modos:
			if modo[2] == 1:
				self.list_tipo.append([str(modo[0]), int(modo[1])])
		self.combo.set_active(0)

if __name__ == "__main__":
	app = Glade()
	Gtk.main()
