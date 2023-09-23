from pba import PBA
from machine import Pin

def test_pbaInit():
    pba = PBA()
    assert isinstance(pba, PBA)

def test_pbaHasLed():
    pba = PBA()
    assert isinstance(pba.led, Pin)

def test_pbaInitFlashesLed(mocker):
    mocker.patch('pba.PBA.flash_led')
    pba = PBA()
    pba.flash_led.assert_called_once()

def test_flashLedCallsOnAndOff(mocker):
    mocker.patch('machine.Pin.on')
    mocker.patch('machine.Pin.off')
    pba = PBA()
    Pin.on.assert_called_once()
    Pin.off.assert_called_once()