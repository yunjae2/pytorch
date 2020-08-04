from torch._six import container_abcs
from itertools import repeat


def _ntuple(n):
    def parse(x):
        if isinstance(x, container_abcs.Iterable):
            return x
        return tuple(repeat(x, n))
    return parse

_single = _ntuple(1)
_pair = _ntuple(2)
_triple = _ntuple(3)
_quadruple = _ntuple(4)


def _reverse_repeat_tuple(t, n):
    r"""Reverse the order of `t` and repeat each element for `n` times.

    This can be used to translate padding arg used by Conv and Pooling modules
    to the ones used by `F.pad`.
    """
    return tuple(x for x in reversed(t) for _ in range(n))


def _list_with_default(out_size, defaults):
    # type: (List[int], List[int]) -> List[int]
    if isinstance(out_size, int):
        return out_size
    if len(defaults) <= len(out_size):
        raise ValueError('Input dimension should be at least {}'.format(len(out_size) + 1))
    return [v if v is not None else d for v, d in zip(out_size, defaults[-len(out_size):])]


range_nr = {}


def log_range(range_key, addr, size, subrange_name=''):
    range_name = range_key + str(range_nr[range_key]) + subrange_name

    print(f"{range_name}:")
    print(f"    addr: {addr}")
    print(f"    size: {size}")


def log_ranges(cls=None, input=None, weight=None, bias=None):
    if cls is None:
        cls_name = 'range'
    else:
        cls_name = type(cls).__name__

    if cls_name not in range_nr:
        range_nr[cls_name] = 0

    if input is not None:
        log_range(cls_name, input.data_ptr(), input.numel() * input.element_size(), 'input')
    if weight is not None:
        log_range(cls_name, weight.data_ptr(), weight.numel() * weight.element_size(), 'weight')
    if bias is not None:
        log_range(cls_name, bias.data_ptr(), bias.numel() * bias.element_size(), 'bias')

    range_nr[cls_name] += 1
