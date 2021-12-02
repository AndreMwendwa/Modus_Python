# -*- coding: iso-8859-15 -*-
"""
Contains a helper class to work with Excel diagrams
"""

import win32com.client


def columnname(colno):
    # colno starting from 0 for the first column!
    if colno <= 25:
        return chr(ord('A') + colno)
    else:
        a,b = divmod(colno, 26)
        return chr(ord('A') + a - 1) + chr(ord('A') + b)

def rangename(rowno,numcols):
    colname = columnname(numcols-1)
    return "%s%d:%s%d" % ("A",rowno, colname, rowno)
    
class Chart:
    """The class represents an Excel diagram with one or several data series.
    Data are added one series at a time and finally show is called to display the diagram.
    """
    def __init__(self, title="", xtitle="", ytitle=""):
        """The constructor for the class.

        title	- string - The diagram title
        xtitle - string - The title for the x axis
        ytitle - string - The title for the y axis
        return - object -	the object.
        """

        self.title = title
        self.xtitle = xtitle
        self.ytitle = ytitle
        
        # acquire application object, which may start application
        self.application = win32com.client.Dispatch("Excel.Application")

        # create new file ('Workbook' in Excel-vocabulary)
        workbook = self.application.Workbooks.Add()

        # build new chart (on seperate page in workbook)
        self.chart = workbook.Charts.Add()
        self.chart.ChartType = 51 # xlColumnClustered
        self.chart.Name = "Plot"

        # initialize worksheet area for series data. Each series y data will be stored
        # in one row, starting with column 2. x values are stored in row 1.
        self.sheet = workbook.Worksheets.Add()
        self.currowno = 2
        
    def addSeries(self, x, y, legend=""):
        """Adds one data series to the diagram.
        
        x	- list -  x values. If several data series are added,
                    only the x values of the first call are accepted as x axis labels,
                    the others are ignored.
        y	- list -  y values
        legend - string - Title for the data series in the legend.
        return - object -	the Excel Series object.
        Example:
        chart.addSeries([1,2,3], [10,20,30], "tenfold")
        """

        # store data in sheet
        xlrangeX = rangename(1, len(x))
        self.sheet.Range(xlrangeX).Value = x
        xlrangeY = rangename(self.currowno, len(y))
        self.sheet.Range(xlrangeY).Value = y
        self.currowno += 1
        
        # create series for chart
        series = self.chart.SeriesCollection().NewSeries()
        series.Values = self.sheet.Range(xlrangeY)
        series.XValues = self.sheet.Range(xlrangeX)
        series.Name = legend
        series.MarkerSize = 3
        return series

    def show(self):
        """makes the diagram visible
        """
        self.chart.HasTitle = True
        self.chart.ChartTitle.Text = self.title
        # setup axes
        xAxis = self.chart.Axes()[0]
        yAxis = self.chart.Axes()[1]
        xAxis.HasMajorGridlines = False
        xAxis.HasTitle = True
        xAxis.AxisTitle.Text = self.xtitle
        yAxis.HasMajorGridlines = True
        yAxis.HasTitle = True
        yAxis.AxisTitle.Text = self.ytitle
        
        # make stuff visible now.
        self.chart.Activate()
        self.application.Visible = True

