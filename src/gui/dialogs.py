from pgu import gui

class alertLengthDialog(gui.Dialog):
    ''' called when the length of the player name and/or password is less than 3 '''
    def __init__(self, **params):
        title = gui.Label("Alert")

        t = gui.Table()

        t.tr()
        t.td(gui.Label("Your name and password must be at least three characters in length!"))

        t.tr()
        t.td(gui.Spacer(10, 20))

        e = gui.Button("OK")
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

# initialize dialogs
AlertLengthDialog = alertLengthDialog()