import os
from io import BytesIO
from array import array

from vbftool import Vbf, VbfVersion, SwPartType, Network, FrameFormat
import vbftool.options as opts


def test_block():
    block = Vbf.create_data_block(0x1200, b'\x33\x22\x55\xAA\xBB\xCC\xDD\xEE\xFF')
    assert block == b'\x00\x00\x12\x00\x00\x00\x00\x09\x33\x22\x55\xaa\xbb\xcc\xdd\xee\xff\xf5\x3f'


def test_reference():
    data = array('B', range(1, 255))
    start_addr = 64 * 1024  # 64 KB
    length = 128 * 1024  # 128 KB
    vbf = Vbf(VbfVersion.VERSION_JLR3_0)
    vbf.add_data(start_addr, data)
    vbf.add_option(opts.Description(['SOP software for X400 AWD',
                                     'Created: 2002-03-14']))
    vbf.add_option(opts.SwPartNumber('318-08832-AB'))
    vbf.add_option(opts.SwPartNumberDID(0xF188))
    vbf.add_option(opts.SwPartType(SwPartType.EXE))
    vbf.add_option(opts.DataFormatIdentifier(0, 0))
    vbf.add_option(opts.Network(Network.CAN_HS))
    vbf.add_option(opts.EcuAddress(0x723))
    vbf.add_option(opts.FrameFormat(FrameFormat.CAN_STANDARD))
    vbf.add_option(opts.Erase([(start_addr, length)]))
    vbf.add_option(opts.Call(start_addr))

    ref_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reference.vbf')
    with open(ref_filename, 'rb') as fp:
        reference = fp.read()

    with open('test.vbf', 'wb') as fp:
        vbf.dump(fp)

    with BytesIO() as fp:
        vbf.dump(fp)
        fp.seek(0)

        assert fp.read() == reference
