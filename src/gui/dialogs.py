from pgu import gui
import global_vars as g
from constants import *

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
        
class alertMessageDialog():
    
    """An alert message box
    
    Example:
        w = TextArea(value="An alert message")
    
    """
    def __init__(self,msg=""):
        
        #count number of newlines in msg
        lines = msg.count('\n')
        # show an alert message
        title = gui.Label("Alert Message")
        main = gui.Container()
        main.add(gui.TextArea(msg,len(msg) * 10, 20 * (lines+1)),0,0)
        
        if msg == 'Your account has been created!':
            def btnAccountCreated(btn):
                g.gameEngine.setState(MENU_LOGIN)
            btn = gui.Button("OK", width=120)
            btn.connect(gui.CLICK, btnAccountCreated, None)
            main.add(btn,20,30)
            
        d = gui.Dialog(title,main)
        d.open()

# initialize dialogs
AlertLengthDialog = alertLengthDialog()