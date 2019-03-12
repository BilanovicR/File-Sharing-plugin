class Converter():
    @staticmethod
    def size_to_string(size):
        count = 0
        f_size = size
        unit = ""

        while(f_size >= 1024):
            f_size /= 1024
            count += 1
        if count == 0:
            unit = " B"
        elif count == 1:
            unit = " KB"
        elif count == 2:
            unit = " MB"
        elif count == 3:
            unit = " GB"
        else:
            unit = " TB"
        
        return (str("%.2f" % f_size) + unit)

        