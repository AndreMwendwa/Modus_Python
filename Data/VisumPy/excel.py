# -*- coding: iso-8859-15 -*-
"""
Contains helper functions for the work with Excel
"""

import win32com.client

def writeTableToExcelFile(listOfColumns, attributeNames, fileName, sheetName=None):
	"""Write table to Excel file
	
	listOfColumns - list(list) - list of columns of data
	attributeNames - list(string) - list of strings of column names
	fileName - string - file name of output Excel file
	sheetName - string - name of work sheet to write data to, default is ActiveSheet
	
	return - null - null
	
	turnVols = turnValueByOrientation(Visum, "VolVehPrT(AP)")
	writeTableToExcelFile(turnVols[0], turnVols[1], "c:/turnVolume.xls")
	"""
	
	#Write Excel file
	excel = win32com.client.Dispatch("Excel.Application")
	excel.Workbooks.Add()
	excel.Visible = True
	if sheetName == None:
		sheet = excel.ActiveSheet
	else:
		sheet = excel.ActiveWorkbook.Sheets(sheetName)
	
	#Get attributes and write excel header name
	for i in range(0, len(attributeNames)):
		sheet.Cells(1,i+1).Value = attributeNames[i]

	#Write attributes
	for i in range(0, len(attributeNames)):
		for j in range(0, len(listOfColumns[0])):
			sheet.Cells(j+2,i+1).Value = listOfColumns[i][j]

	#Clean up columns
	for i in range(0, len(attributeNames)):
		sheet.Columns(i+1).EntireColumn.AutoFit()

	#Save and close
	excel.ActiveWorkbook.SaveAs(fileName)
	excel.Quit()
	
def writeTablesToExcelFile(listOfTables, fileName):
	"""Write tables to an Excel file
	10/20/07 fixed deleting of sheet2 and sheet3 to be compatible with Excel 2000
	
	This function writes tables to an Excel file.  Each table entry 
	must be a list with 3 items - table data, attributes, sheetName
	
	listOfTables - list(list(list), list(string), string) - table data
	fileName - string - file name of output Excel file
	
	return - null - null
	
	Example of writing node, link and zone attributes
	uses the networkObjectAttributeList function from VisumPy.reports
	attributesNode = ["No","Name"]
	nodeData = networkObjectAttributeList(Visum.Net.Nodes, attributesNode)
	nodeTable = [nodeData[0], attributesNode, "Node"]
	
	attributesLink = ["FromNodeNo","ToNodeNo","VolVehPrt(AP)"]
	linkData = networkObjectAttributeList(Visum.Net.Links, attributesLink)
	linkTable = [linkData[0], attributesLink, "Link"]
	
	attributesZone = ["No","Name","XCOORD","YCOORD"]
	zoneData = networkObjectAttributeList(Visum.Net.Zones, attributesZone)
	zoneTable = [zoneData[0], attributesZone, "Zone"]
	
	listOfTables = [nodeTable, linkTable, zoneTable] 
	writeTablesToExcelFile(listOfTables, "c:/report.xls")
	"""
	
	#Create Excel 
	excel = win32com.client.Dispatch("Excel.Application")
	excel.Workbooks.Add()
	excel.Visible = True
	
	#Delete sheet 2 and 3 if available
	excel.DisplayAlerts = False
	numSheets = excel.ActiveWorkbook.Sheets.Count
	ids = range(numSheets)
	ids.reverse()
	for i in ids:
		if i > 0:
			excel.ActiveWorkbook.Sheets(i + 1).Delete()
	excel.DisplayAlerts = True
	
	#Create sheets
	numTables = len(listOfTables)
	for i in range(0, numTables):
	
		tableData = listOfTables[i][0]
		attributeNames = listOfTables[i][1]
		sheetName = listOfTables[i][2]
		
		if i == 0: 
			excel.ActiveWorkbook.Sheets(1).Name = sheetName
		else: 
			excel.ActiveWorkbook.Sheets.Add(None, excel.ActiveSheet)
			excel.ActiveSheet.Name = sheetName
	
		#Get active sheet
		sheet = excel.ActiveSheet
	
		#Get attributes and write excel header name
		for i in range(0, len(attributeNames)):
			sheet.Cells(1,i+1).Value = attributeNames[i]

		#Write attributes
		for i in range(0, len(attributeNames)):
			for j in range(0, len(tableData[0])):
				sheet.Cells(j+2,i+1).Value = tableData[i][j]

		#Clean up columns
		for i in range(0, len(attributeNames)):
			sheet.Columns(i+1).EntireColumn.AutoFit()

	#Save and close
	excel.ActiveWorkbook.SaveAs(fileName)
	excel.Quit()
	
