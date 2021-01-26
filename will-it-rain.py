import sys
import pymsgbox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot,Qt
from pyowm.utils import timestamps
from pyowm.owm import OWM
def startwheater(apikey):
    tomorrow = timestamps.tomorrow()
    owm = OWM(apikey)
    mgr = owm.weather_manager()
    cname = 'Rome'
def predict(cityname):
    three_h_forecaster = mgr.forecast_at_place(cityname, '3h')
    return three_h_forecaster.will_be_rainy_at(tomorrow)
def showerror(title='Error',shorttext='An error happened',infotext=''):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(shorttext)
    msg.setInformativeText(infotext)
    msg.setWindowTitle(title)
    msg.exec_()
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Will it rain?'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.hbox = QVBoxLayout()
        self.labelB = QLabel(self)
        self.labelB.setText(cname)
        self.labelB.setAlignment(Qt.AlignCenter)
        button = QPushButton(f'Will it rain tomorrow?', self)
        button.setToolTip('This is an example button')
        button2 = QPushButton('Set city', self)
        button2.setToolTip('This is an example button')
        button.clicked.connect(self.on_click)
        button2.clicked.connect(self.selectcity)
        self.hbox.addWidget(self.labelB)
        self.hbox.addWidget(button)
        self.hbox.addWidget(button2)
        self.setLayout(self.hbox)
        self.show()

    @pyqtSlot()
    def on_click(self):
        rain = predict(cname)
        if rain: ris = 'YES'
        else: ris = 'NO'
        try: self.labelA.setText(ris)
        except:
            self.labelA = QLabel(self)
            self.labelA.setText(ris)
            self.labelA.setStyleSheet("border-radius: 2em;border: 0.2em dotted;margin-top: 1em;padding: 0.2em")
            self.labelA.setAlignment(Qt.AlignCenter)
            self.labelA.setFont(QFont("Roboto", 56, QFont.Bold))
            self.hbox.addWidget(self.labelA)
        self.labelB.setText(cname)
    @pyqtSlot()
    def selectcity(self):
        cityreg = owm.city_id_registry()
        while True:
            text, okPressed = QInputDialog.getText(self, "City Name","City Name ( e.g. London, GB ):", QLineEdit.Normal, "")
            if okPressed and text != '':
                if ',' in text:
                    countrycode = text.split(',')[1].strip()
                    city = text.split(',')[0].strip()
                    matchlist = cityreg.ids_for(city, country=countrycode)
                else:
                    matchlist = cityreg.ids_for(text)
                if len(matchlist) == 0:
                    showerror(title='No city found',shorttext='No city has been found.', infotext='Check your spelling.')
                else:
                    global cname
                    try:
                        cname = city
                    except:
                        cname = text + ',' + matchlist[0][2]
                    self.labelB.setText('Click to get forecast for ' + cname)
                    
                    break
            else:
                showerror(title='City name',shorttext='City name entry is blank', infotext='Enter a City Name')
if __name__ == '__main__':
    startwheater('Place your OWM api key here')
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
