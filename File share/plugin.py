from plugin_framework.plugin import Plugin
from .widget.file_share_widget import FileShareWidget
from .model.setup import Setup

class Main(Plugin):
    def __init__(self, plugin_specification):
        super().__init__(plugin_specification)

    def activate(self):
        pass
        #print("File share activated")
        #ovde inicijalizuj Device, Broadcaster, Setup klasu i sta sve treba
        #self.setup = Setup()
        #da bi njihovim metodama mogla da pristupas preko widgeta i menjas sta treba preko gui
        #drzi se dijagrama klasa!!!
    
    def deactivate(self):
        print("File share deactivated")

    def get_widget(self, parent=None):
        #print("Viewing file share widget")
        return FileShareWidget(parent), None, None


