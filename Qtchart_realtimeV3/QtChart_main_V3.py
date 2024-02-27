########################################################################
# Basic Library for PYQT5
########################################################################
import os  
import sys # We need sys so that we can pass argv to QApplication
from PyQt5.QtWidgets import* 
from PyQt5.QtGui import* 
from PyQt5.QtCore import* 

########################################################################
# Specific Library for project
########################################################################
from random import randint, random, uniform
import math

########################################################################
# Special Class [WIDGET FIGURE]
########################################################################
from PyQt5.QtChart import * 

########################################################################
# Import python file from Ui File
########################################################################
from ui_mainwindow import Ui_MainWindow

########################################################################
# Main Class
########################################################################
class MainWindow(QMainWindow):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QMainWindow.__init__(self)
		self.my_dash = Ui_MainWindow()
		self.my_dash.setupUi(self)
		
		###### Set-up : Widgets  | Special Fuctions ####################
		self.setupWidget()
		
		###### Init Timers: CLOCK | SAMPLER ############################
		self.iniClock()
		self.iniSampler()
		self.show()
		sys.exit(self.app.exec_())
	
	####################################################################
	# TIMER UPDATE CLOCK 
	####################################################################
	def iniClock(self):
		self.timerClk = QTimer()
		self.timerClk.setInterval(1000)
		self.timerClk.timeout.connect(self.showTime)
		self.timerClk.start()
		
	def showTime(self):
		current_time = QTime.currentTime()
		time = current_time.toString('HH:mm:ss')
		self.my_dash.label_hora.setText(time)
		now = QDate.currentDate()
		date = now.toString(Qt.ISODate)
		self.my_dash.label_fecha.setText(date)
	
	####################################################################
	# SET UP GRAPHS
	####################################################################
	def setupWidget(self):
		self.ndata = 120
		self.ndatax = 120
		### CREATE  CHART ##############################################
		fontT = QFont('Open Sans')
		fontT.setPixelSize(18)
		fontT.setBold(True)
		
		fontL = QFont('Open Sans')
		fontL.setPixelSize(16)
		fontL.setBold(True)
		
		self.chart =  QChart()
		self.chart.setTitle("Line Chart Example")
		self.chart.setTitleFont(fontT)
		self.chart.setTitleBrush(QBrush(QColor("#FF6060")))
		self.chart.setBackgroundBrush(QBrush(QColor("#101010")))
		
		self.chart.legend().setVisible(True)
		self.chart.legend().setAlignment(Qt.AlignBottom)
		self.chart.legend().setFont(fontL)
		self.chart.legend().setLabelColor(QColor("#B0B0B0"))
		self.chart.legend().setBackgroundVisible(False)
		#self.chart.legend().setBrush(QBrush(QColor("#b0b0b0")))
		#self.chart.legend().setPen(QPen(QColor("#00ff00")))
		
		### CREATE SERIES AND ADD TO CHART #############################
		self.seriesA = QLineSeries(self)
		self.seriesB = QLineSeries(self)
		self.seriesC = QLineSeries(self)
		self.seriesD = QLineSeries(self)
		
		self.seriesA.setName("linea 1")
		self.seriesB.setName("linea 2")
		self.seriesC.setName("linea 3")
		self.seriesD.setName("linea 4")
		
		pen = QPen()
		pen.setWidth(2)
		self.seriesA.setPen(pen)
		self.seriesB.setPen(pen)
		self.seriesC.setPen(pen)
		self.seriesD.setPen(pen)
		
		colorseriesA = QColor("#ffa560")
		colorseriesB = QColor("#A5FF00")
		colorseriesC = QColor("#00A5FF")
		colorseriesD = QColor("#00FFA5")
		
		self.seriesA.setColor(colorseriesA)
		self.seriesB.setColor(colorseriesB)
		self.seriesC.setColor(colorseriesC)
		self.seriesD.setColor(colorseriesD)
		
		self.chart.addSeries(self.seriesA)
		self.chart.addSeries(self.seriesB)
		self.chart.addSeries(self.seriesC)
		self.chart.addSeries(self.seriesD)
		
		### CREATE X AXIS AND ATTACH SERIES TO AXIS#####################
		fontA = QFont('Open Sans')
		fontA.setPixelSize(14)
		fontA.setBold(True)
		
		### AXIS X IN EPOCH TIME #######################################
		self.axisX = QDateTimeAxis()
		self.axisX.setFormat("mm:ss.z")
		#self.axisX.setMax(QDateTime.currentDateTime())
		#self.axisX.setMin(QDateTime.currentDateTime().addSecs(-1*self.ndata/2))
		self.axisX.setTickCount(6)
		self.axisX.setGridLinePen(QPen(QColor("#808080")))
		self.axisX.setLabelsColor(QColor("#FFFFFF"))
		self.chart.addAxis(self.axisX, Qt.AlignBottom)
		
		self.seriesA.attachAxis(self.axisX);
		self.seriesB.attachAxis(self.axisX);
		self.seriesC.attachAxis(self.axisX);
		self.seriesD.attachAxis(self.axisX);

		### AXIS Y LEFT#################################################
		self.axisY = QValueAxis()
		self.axisY.setRange(-50, 50)
		self.axisY.setTickCount(8)
		self.axisY.setLinePenColor(self.seriesA.pen().color())
		self.axisY.setLabelsColor(colorseriesA)
		self.axisY.setLabelsFont(fontA)
		self.axisY.setTitleText("VOLTS")
		self.axisY.setTitleBrush(QBrush(colorseriesA))
		self.chart.addAxis(self.axisY, Qt.AlignLeft)
		self.seriesA.attachAxis(self.axisY);
		
		self.axisY = QValueAxis()
		self.axisY.setRange(-40, 40)
		self.axisY.setTickCount(8)
		self.axisY.setLinePenColor(self.seriesC.pen().color())
		self.axisY.setLabelsColor(colorseriesC)
		self.axisY.setLabelsFont(fontA)
		self.axisY.setTitleText("AMPS")
		self.axisY.setTitleBrush(QBrush(colorseriesC))
		self.chart.addAxis(self.axisY, Qt.AlignLeft)
		self.seriesC.attachAxis(self.axisY);
		
		### AXIS Y RIGHT ###############################################
		self.axisYX = QValueAxis()
		self.axisYX.setRange(-50, 50)
		self.axisYX.setTickCount(8)
		self.axisYX.setLinePenColor(self.seriesB.pen().color())
		self.axisYX.setLabelsColor(colorseriesB)
		self.axisYX.setLabelsFont(fontA)
		self.chart.addAxis(self.axisYX, Qt.AlignRight)
		self.seriesB.attachAxis(self.axisYX);
		
		self.axisYX = QValueAxis()
		self.axisYX.setRange(-60, 60)
		self.axisYX.setTickCount(8)
		self.axisYX.setLinePenColor(self.seriesD.pen().color())
		self.axisYX.setLabelsColor(colorseriesD)
		self.axisYX.setLabelsFont(fontA)
		self.chart.addAxis(self.axisYX, Qt.AlignRight)
		self.seriesD.attachAxis(self.axisYX)
		
		self.dataSA = [0]*self.ndata
		self.dataSB = [0]*self.ndata
		self.dataSC = [0]*self.ndata
		self.dataSD = [0]*self.ndata
		
		start_timeMS = QDateTime.currentMSecsSinceEpoch()
		self.dataTime = [start_timeMS]*self.ndata

	####################################################################
	# SAMPLER 
	####################################################################
	def iniSampler(self):
		self.timer = QTimer()
		self.timer.setInterval(500)
		self.timer.timeout.connect(self.lecturaData)
		self.timer.start()
		
	####################################################################
	# READ DATA FROM PLC - SENSORS- ARDUINO
	####################################################################
	def lecturaData(self):
		### FLAG TO PLOT IN X AXIS #####################################
		self.timeTESTE = QDateTime.currentMSecsSinceEpoch()
		
		### READ DATA FROM EXTERNAL DEVICE #############################
		ah1 = 10*uniform(-1,1) +40
		ah2 = 10*uniform(-1,1) -10
		ah3 = 10*uniform(-1,1) -30
		ah4 = 10*uniform(-1,1) +20
		self.update_plot_data(ah1,ah2,ah3,ah4)
		
	def update_plot_data(self,ah1,ah2,ah3,ah4 ):
		### REMOVE LAST DATA AND INSERT NEW DATA########################
		self.dataSA = self.dataSA[1:] + [ah1]
		self.dataSB = self.dataSB[1:] + [ah2]
		self.dataSC = self.dataSC[1:] + [ah3]
		self.dataSD = self.dataSD[1:] + [ah4]
		self.dataTime = self.dataTime[1:] + [self.timeTESTE]
		
		#print(QDateTime.currentDateTime())
		#print(QDateTime.currentMSecsSinceEpoch())
		
		### CLEAR SERIES DATA ##########################################
		self.seriesA.clear()
		self.seriesB.clear()
		self.seriesC.clear()
		self.seriesD.clear()
		
		### INSERT NEW VALUES IN SERIES ################################
		for i, value in enumerate(self.dataSA):
			self.seriesA.append(self.dataTime[i], value)
		for i, value in enumerate(self.dataSB):
			self.seriesB.append(self.dataTime[i], value)
		for i, value in enumerate(self.dataSC):
			self.seriesC.append(self.dataTime[i], value)
		for i, value in enumerate(self.dataSD):
			self.seriesD.append(self.dataTime[i], value)
		
		### UPDATE LABES X AXIS ########################################
		self.axisX.setMax(QDateTime.currentDateTime())
		self.axisX.setMin(QDateTime.currentDateTime().addSecs(-1*60))
		
		# addSecs(-1*self.ndata*[timeSampler]/[1000miliSeconds])) 
		
		### SHOW CHART #################################################
		self.my_dash.graphicsView.setRenderHint(QPainter.Antialiasing)
		self.my_dash.graphicsView.setChart(self.chart)

########################################################################
# Run Routine
########################################################################

if __name__ == '__main__':
	MainWindow()

