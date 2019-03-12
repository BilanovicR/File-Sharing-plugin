class PluginInterface:
    def __init__(self):
        super().__init__()
    
    def activate(self):
        raise NotImplementedError()

    def deactivate(self):
        raise NotImplementedError()

    def get_widget(self):
        raise NotImplementedError("Nije implementirana metoda get_widget!")
