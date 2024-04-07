from pwn import p64, u64

class StreamO():
    def __init__(self, target, do_print=True):
        self.target = target
        self.__print = do_print

    def set_target(self, target):
        self.target = target

    def stop_printing(self):
        self.__print = False

    def start_printing(self):
        self.__print = True

    def set_printing(self, do_print):
        self.__print = do_print

    def print(self, byte_text):
        if self.__print:
            print(byte_text.strip().decode('utf-8'))

    def puntil(self, pattern):
        recv_b = self.target.recvuntil(pattern)
        self.print(recv_b)

    def pline(self, n=1):
        for _ in range(n):
            self.print(self.target.recvline())

    def getline(self, n=1, timeout=None, dtype="str"):
        kwargs = {} if timeout is None else {"timeout":timeout}
        res_bytes = b""
        for _ in range(n):
            res_bytes += self.target.recvline(**kwargs).strip()
        if dtype == "str":
            try:
                res_str = res_bytes.decode('utf-8')
            except UnicodeDecodeError:
                pass
            return res_str
        return res_bytes

# they are from https://www.falatic.com/index.php/108/python-and-bitwise-rotation
def rol(b, n=8, max_bits=64):
    i = u64(b)
    i = (i << n % max_bits) & (2**max_bits-1) | ((i & (2**max_bits-1)) >> (max_bits - (n % max_bits)))
    return p64(i)

def ror(b, n=8, max_bits=64):
    i = u64(b)
    i = ((i & (2**max_bits-1)) >> n % max_bits) | (i << (max_bits - (n % max_bits)) & (2**max_bits-1))
    return p64(i)
