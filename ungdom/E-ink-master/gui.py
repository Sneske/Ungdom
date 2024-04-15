# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Waveshare E-ink demo", pos = wx.DefaultPosition, size = wx.Size( 431,249 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu2 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem1 )

		self.m_menubar1.Append( self.m_menu2, u"File" )

		self.SetMenuBar( self.m_menubar1 )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer1.SetMinSize( wx.Size( 0,0 ) )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer3.SetMinSize( wx.Size( 0,0 ) )
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Indtast tekst:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer3.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.eink_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.eink_txt, 0, wx.ALL|wx.EXPAND, 5 )

		m_radioBox1Choices = [ u"Sort", u"Rød" ]
		self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, u"Farvevalg", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox1.SetSelection( 0 )
		bSizer3.Add( self.m_radioBox1, 0, wx.ALL, 5 )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Send til e-Ink display", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button1, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer3, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.afslut, id = self.m_menuItem1.GetId() )
		self.m_button1.Bind( wx.EVT_BUTTON, self.send_to_eink )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def afslut( self, event ):
		event.Skip()

	def send_to_eink( self, event ):
		event.Skip()


