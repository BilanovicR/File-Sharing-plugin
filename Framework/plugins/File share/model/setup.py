class Setup():
    def __init__(self):
        self._port = 17116
        self._name = "My device"
        self._download_dir = "downloads/"

    def get_port(self):
        return self._port

    def set_port(self, port):
        self._port = port

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_download_dir(self):
        return self._download_dir

    def set_download_dir(self, download_dir):
        self._download_dir = download_dir

