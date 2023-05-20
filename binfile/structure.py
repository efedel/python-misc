import struct

class ByteOrder(object):
    """Endianness and size format for structures."""
    Native          = "@"       # Native format, native size
    StandardNative  = "="       # Native format, standard size
    LittleEndian    = "<"       # Standard size
    BigEndian       = ">"       # Standard size
    
class Element(object):
    """A single element in a struct."""
    def __init__(self, typecode):
        self.typecode = typecode
        self.size = struct.calcsize(typecode)

    def __len__(self):
        return self.size

    def decode(self, format, s):
        """Additional decode steps once converted via struct.unpack"""
        return s

    def encode(self, format, val):
        """Additional encode steps to allow packing with struct.pack"""
        return val

    def __str__(self):
        return self.typecode

    def __call__(self, num):
        """Define this as an array of elements."""
        # Special case - strings already handled as one blob.
        if self.typecode in 'sp':
            # Strings handled specially - only one item
            return Element('%ds' % num)
        else:
            return ArrayElement(self, num)

    def __getitem__(self, num): return self(num)

class ArrayElement(Element):
    def __init__(self, basic_element, num):
        super(ArrayElement, self).__init__(self,
                '%ds' % (len(basic_element) * num))
        self.num = num
        self.basic_element = basic_element

    def decode(self, format, s):
        # NB. We use typecode * size, not %s%s' % (size, typecode), 
        # so we deal with typecodes that already have numbers,  
        # ie 2*'4s' != '24s'
        return [self.basic_element.decode(format, x) for x in  
                    struct.unpack('%s%s' % (format, 
                            self.num * self.basic_element.typecode),s)]

    def encode(self, format, vals):
        fmt = format + (self.basic_element.typecode * self.num)
        return struct.pack(fmt, *[self.basic_element.encode(format,v) 
                                  for v in vals])

class EmbeddedStructElement(Element):
    def __init__(self, structure):
        super(EmbeddedStructElement, self).__init__(self,
                '%ds' % structure._struct_size)
        self.struct = structure

    # Note: Structs use their own endianness format, not their parent's
    def decode(self, format, s):
        return self.struct(s)

    def encode(self, format, s):
        return str(self.struct)
    def __repr__(self):
        return repr(self.struct)

name_to_code = {
    'Char'             : 'c',
    'Byte'             : 'b',
    'UnsignedByte'     : 'B',
    'Int'              : 'i',
    'UnsignedInt'      : 'I',
    'Short'            : 'h',
    'UnsignedShort'    : 'H',
    'Long'             : 'l',
    'UnsignedLong'     : 'L',
    'String'           : 's',  
    'PascalString'     : 'p',  
    'Pointer'          : 'P',
    'Float'            : 'f',
    'Double'           : 'd',
    'LongLong'         : 'q',
    'UnsignedLongLong' : 'Q',
    }

class Type(object):
    def __getattr__(self, name):
        return Element(name_to_code[name])

    def Struct(self, struct):
        return EmbeddedStructElement(struct)
        
Type=Type()

# XXX do we need to create a new Element object everytime? can't we just get 
# away with making a single instance of each type?
Int8     = Element('b') #Type.Byte
Int16    = Element('h') #Type.Short
Int32    = Element('i') #Type.Int
Int64    = Element('q') #Type.LongLong
uInt8    = Element('B') #Type.UnsignedByte
uInt16   = Element('H') #Type.UnsignedShort
uInt32   = Element('I') #Type.UnsignedInt
uInt64   = Element('Q') #Type.UnsignedLongLong
Character= Element('c') #Type.Char
String   = Element('s') #Type.String
Struct   = lambda s: EmbeddedStructElement(s)

class MetaStruct(type):
    def __init__(cls, name, bases, d):
        type.__init__(cls, name, bases, d)
        if hasattr(cls, '_struct_fmt'):  # Allow extending by inheritance
            cls._struct_info = list(cls._struct_info) # use copy.
        else:
            cls._struct_fmt=''
            cls._struct_info=[]     # name / element pairs

        elems = cls._fields_

        cls._struct_fmt += ''.join(str(v) for (k,v) in elems)
        cls._struct_info += elems
        cls._struct_size = struct.calcsize(cls._byteorder + cls._struct_fmt)

class Structure(object):
    """Represent a binary structure."""
    __metaclass__=MetaStruct
    _byteorder = ByteOrder.Native  # Default to native format, native size
    _fields_ = []

    def __init__(self, _data=None, **kwargs):
        if _data is None:
            _data ='\0' * self._struct_size

        ldata = len(_data)
        if ldata < self._struct_size:
            _data += '\0' * (self._struct_size - ldata)
        elif ldata > self._struct_size:
            _data = _data[:self._struct_size]
            
        fieldvals = zip(self._struct_info, struct.unpack(self._byteorder + 
                                             self._struct_fmt, _data))
        for (name, elem), val in fieldvals:
            setattr(self, name, elem.decode(self._byteorder, val))
        
        for k,v in kwargs.iteritems():
            setattr(self, k, v)

    def _pack(self):
        return struct.pack(self._byteorder + self._struct_fmt, 
            *[elem.encode(self._byteorder, getattr(self, name)) 
                for (name,elem) in self._struct_info])                

    def __str__(self):
        return self._pack()
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,', '.join([
            '%s=%r'%(k,getattr(self,k))
            for k,v in self._struct_info
            if not callable(getattr(self, k)) and not k.startswith('__')]))

    def __len__(self):
        return self._struct_size

class Union(Structure):
    _max = ('', None)
    def __init__(self, _data=None, **kwargs):
        max = 0
        for (name, elem) in self._struct_info:
            if len(elem) > max:
                max = len(elem)
                self._max = (name, elem)

        if _data == None:
            _data = '\0' * len(self._max[1])

        for (name, elem) in self._struct_info:
            if issubclass(Element, elem):
                val = struct.unpack(self._byteorder + str(elem),
                        _data[:len(elem)])
            else:
                val = _data
            setattr(self, name, elem.decode(self._byteorder, val))

    def _pack(self):
        return struct.pack(self._byteorder + str(self._max[1]),
                elem.encode(self._byteorder, getattr(self, self._max[0])))
