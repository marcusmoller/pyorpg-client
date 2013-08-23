from pgu import gui
import global_vars as g
from constants import *

def alertMessageDialog(msg='', title=''):
    # show an alert message
    if title is '':
        title = gui.Label('Alert Message')
    else:
        title = gui.Label(title)

    mainTable = gui.Table()

    mainTable.tr()
    mainTable.td(gui.Spacer(10, 10))

    mainTable.tr()
    mainTable.td(gui.Label(msg))

    mainTable.tr()
    mainTable.td(gui.Spacer(10, 20))

    d = gui.Dialog(title, mainTable)

    # handle alert messages differently on some alerts
    if msg == 'Your account has been created!':
        def btnAccountCreated(btn):
            g.gameEngine.setState(MENU_LOGIN)
            d.close()

        btn = gui.Button('OK', width=120)
        btn.connect(gui.CLICK, btnAccountCreated, None)

    else:
        # simple close button
        def btnOk(btn):
            d.close()

        btn = gui.Button('OK', width=120)
        btn.connect(gui.CLICK, btnOk, None)

    # add button to alert message
    mainTable.tr()
    mainTable.td(btn)

    # show the message
    d.open()
