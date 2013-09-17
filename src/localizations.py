import gettext
import locale

import global_vars as g
 
def initLocalization():
    '''prepare l10n'''
    locale.setlocale(locale.LC_ALL, '') # use user's preferred locale
    # take first two characters of country code
    loc = locale.getlocale()
    filename = "/res/messages_%s.mo" % locale.getlocale()[0][0:2]
     
    try:
        print "Opening message file %s for locale %s" % (filename, loc[0])
        trans = gettext.GNUTranslations(open(g.dataPath + filename, "rb" ) )
    except IOError:
        print "Locale not found. Using default messages"
        trans = gettext.NullTranslations()
     
    trans.install()