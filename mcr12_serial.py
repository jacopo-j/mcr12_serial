#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

class BarcodeScanner(serial.Serial):
    NUL = STOP_SCANNING = 0x00
    CMD = SCANNER_CTRL = SCAN_FOREVER = 0x01
    STX = SET = SCAN_TIMEOUT = 0x02
    ETX = SAVE_CONF = 0x03
    CONFIG_FLAG = 0x82
    HFF = 0xFF
    HAA = 0xAA
    H16 = 0x100
    H85 = 0x55
    SAVE_CMD = [CMD, SAVE_CONF, HAA, H85]

    TIMEOUT_VALUE_ERR = "timeout must be between 0 and 65535 milliseconds"
    TIMEOUT_TYPE_ERR = "timeout must be an integer, not '{}'"
    CONFIG_TYPE_ERR = "configuration code must a string, not '{}'"
    CONFIG_LEN_ERR = "length of the configuration code must be between 1 and 10 characters"
    SCAN_TIMED_OUT = "operation timed out."

    def __init__(self, dev, baudrate=9600, timeout=None):
        super().__init__(dev, baudrate, 8, serial.PARITY_NONE, timeout=timeout)

    def _checksum(self, data_bytes):
        # Input: from byte 1 to byte 13 (index 0).
        byte_sum = self.STX + self.ETX + sum(data_bytes)
        return self.H16 - (byte_sum & self.HFF)

    def _build_bin_str(self, data_bytes):
        bin_data = [self.STX] + data_bytes + [self.NUL] * (13 - len(data_bytes))
        bin_data += [self.ETX, self._checksum(data_bytes)]
        return bytes(bin_data)

    def _send_command(self, command):
        self.flushInput()
        self.flushOutput()
        self.write(command)
        self.flush()

    def scan(self, timeout=0):
        # Timeout in milliseconds. 0 = no timeout.
        if not isinstance(timeout, int):
            raise TypeError(self.TIMEOUT_TYPE_ERR.format(type(timeout).__name__))
        if (timeout > 65535) or (timeout < 0):
            raise ValueError(self.TIMEOUT_VALUE_ERR)
        data_bytes = [self.CMD, self.SCANNER_CTRL]
        if (timeout == 0):
            data_bytes.append(self.SCAN_FOREVER)
            self.timeout = None
        else:
            high_tx, low_tx = divmod(timeout, self.H16)
            data_bytes.append(self.SCAN_TIMEOUT)
            data_bytes.append(low_tx)
            data_bytes.append(high_tx)
            self.timeout = timeout / 1000
        self._send_command(self._build_bin_str(data_bytes))
        scan_data = self.readline()
        if (len(scan_data) == 0):
            raise TimeoutError(self.SCAN_TIMED_OUT)
        return scan_data.decode().strip()

    def stop(self):
        data_bytes = [self.CMD, self.SCANNER_CTRL, self. STOP_SCANNING]
        self._send_command(self._build_bin_str(data_bytes))

    def config(self, conf_code):
        if not isinstance(conf_code, str):
            raise TypeError(self.CONFIG_TYPE_ERR.format(type(conf_code).__name__))
        conf_bytes = []
        for char in conf_code:
            conf_bytes.append(ord(char))
        if (len(conf_bytes) > 10) or (len(conf_bytes) == 0):
            raise ValueError(self.CONFIG_LEN_ERR)
        data_bytes = [self.SET, len(conf_bytes) + 1, self.CONFIG_FLAG]
        data_bytes += conf_bytes
        self._send_command(self._build_bin_str(data_bytes))
        self._send_command(self._build_bin_str(self.SAVE_CMD))

