import io

class ConsoleRedirect(io.TextIOBase):
    def __init__(self, write_callback):
        self.write_callback = write_callback

    def write(self, msg):
        if msg.strip():
            self.write_callback(msg)

    def flush(self):
        pass  # Needed for compa