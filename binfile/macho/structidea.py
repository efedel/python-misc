

class Foo(Structure):
    __struct__ ()

class Bar(Structure):
    __struct__ = (
        ('header',  Foo),
        ('new',     uInt32),
    )

def unpack():
    if type(fmt) not type(''):
        value = fmt(data[off:])
        off += len(value)
    else:
        # do normal unpack
