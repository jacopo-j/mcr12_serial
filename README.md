## Introduction

This is a Python 3 module for controlling the so called "MCR12" barcode scanner module via USB serial port emulation. The MCR12 is sold as standalone module, [for example on Adafruit](https://www.adafruit.com/product/1202), and it is also the module on which some barcode scanner, [such as this one](https://www.amazon.com/dp/B01FVYVX5A), are based.


## Usage

```python
from mcr12_serial import BarcodeScanner

bcd = BarcodeScanner("/path/to/serial/device", baudrate=9600)

barcode1 = bcd.scan()  # Same as bcd.scan(0)
# The scanner will start scanning indefinitely until a barcode is
# scanned.

barcode2 = bcd.scan(5000)
# The scanner will start scanning. If after 5000 milliseconds no
# barcode has been scanned, a TimeoutError is raised.

bcd.stop()
# Stop scanning. Not really useful here as the scanner stops scanning
# automatically after a barcode has been scanned or after the timeout
# has expired. However it may be useful if you call the scan() method
# asynchronously or if you need to handle a KeyboardInterrupt to stop
# scanning after calling the scan() method.

bcd.config("013300")
# Edit the scanner configuration. "013300" must be replaced with a
# configuration code.
```

### Configuration codes

You can find configuration codes on the [MCR 12 Manual](https://cdn-shop.adafruit.com/product-files/1203/MCR12_Scanner_Manual.pdf). They are written under each configuration barcode.


## Copyright & Disclaimer

Copyright (c) 2017 Jacopo Jannone

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.