from codecs import utf_8_decode, utf_8_encode

class DummyBase():
    def prepare_input(self, string):
        self.in_.seek(0)
        self.in_.write(utf_8_encode(string + '\n// END\n')[0])
        self.in_.truncate()
        self.in_.seek(0)

    def get_output(self):
        r = utf_8_decode(self.out.getvalue())[0]
        self.out.seek(0)
        self.out.truncate()
        if not r.endswith('\n// END\n'):
            raise Exception('end marker not found')
        return r[:-8]
