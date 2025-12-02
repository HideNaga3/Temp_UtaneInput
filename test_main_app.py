import pytest
from PyQt5.QtWidgets import QApplication
from MAIN_APP import MyMainWindow
import sys

@pytest.fixture(scope='session', autouse=True)
def app():
    import sys
    app = QApplication(sys.argv)
    yield app

def test_is_post_number_kuromaru():
    app = QApplication(sys.argv)
    mywindow = MyMainWindow()
    assert mywindow.is_post_number_kuromaru('123-4567') == True
    assert mywindow.is_post_number_kuromaru('1234567') == False

test_is_post_number_kuromaru()