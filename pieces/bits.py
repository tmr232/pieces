import wrapt


def trim_byte(value):
    return value & 0xFF


@wrapt.decorator
def return_byte(wrapped, instance, args, kwargs):
    return_value = wrapped(*args, **kwargs)
    return trim_byte(return_value)


@return_byte
def shift_left_byte(value, amount):
    return value << amount


SHL8 = shift_left_byte


@return_byte
def shift_arithmetic_right_byte(value, amount):
    return value >> amount


SAR8 = shift_arithmetic_right_byte


@return_byte
def shift_right_byte(value, amount):
    return trim_byte(value) >> amount


SHR8 = shift_right_byte


@return_byte
def rotate_left_byte(value, amount):
    # ROL(X) = SHL(X) | SHR(8 - X)
    amount %= 8
    value = trim_byte(value)
    return SHL8(value, amount) | SHR8(value, 8 - amount)


ROL8 = rotate_left_byte

ROR8 = lambda value, amount: ROL8(value, -amount)

if __name__ == '__main__':
    print bin(0b11001100), bin(ROL8(0b11001100, 1)), bin(ROR8(0b11001100, 1))