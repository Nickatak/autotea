import mock

import pytest

from autotea.reader import TemperatureReader


@pytest.mark.parametrize(
    "attr_name",
    (
        "base_dir",
        "fail_loud",
        "file_path",
    ),
)
@mock.patch("os.system")
@mock.patch("glob.glob", return_value=["test-dir"])
def test_init_should_set_attributes(glob_mock, system_mock, attr_name):
    reader = TemperatureReader()

    assert hasattr(reader, attr_name)

@mock.patch("os.system")
@mock.patch("glob.glob", return_value=[])
def test_init_should_raise_exc_if_no_devices(glob_mock, system_mock):
    with pytest.raises(IOError) as e:
        reader = TemperatureReader()

    assert str(e.value) == "Could not locate device interface.  Please see the following link to make sure you've enbaled 1-wire interfaces: https://www.raspberrypi-spy.co.uk/2013/03/raspberry-pi-1-wire-digital-thermometer-sensor/."
