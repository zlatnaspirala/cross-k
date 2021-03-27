
from kivy.uix.label import Label
from kivy.core.text import FontContextManager as FCM

class FontFactory():

    def __init__(self, **kwargs):
        # get any files into images directory
        self.engineConfig = kwargs.get("engineConfig")

        print(" self.engineConfig.currentProjectName " , self.engineConfig.currentProjectName)
        self.constructCtxName = 'system://myapp' # + self.engineConfig.currentProjectName

        # Create a font context containing system fonts + one custom TTF
        FCM.create(self.constructCtxName)
        self.family = FCM.add_font('spacetime.ttf')

        # These are now interchangeable ways to refer to the custom font:
        #lbl1 = Label(font_context=constructCtxName, family_name=family)
        #lbl2 = Label(font_context=constructCtxName, font_name='spacetime.ttf')
        # You could also refer to a system font by family, since this is a
        # system:// font context
        #lbl3 = Label(font_context='system://myapp', family_name='Arial')
        # Explore and make handler for font avable listin 2.0