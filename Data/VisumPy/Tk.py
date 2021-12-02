# -*- coding: iso-8859-15 -*-
"""
Contains a Tkinter widget class for a list box (with scroll bar)
that contains all instances of a certain network object type and lets the
user select one or several of those. And a class for a Tk progress dialog 
"""

import Tkinter as Tk
import tkFileDialog
import tkMessageBox
from VisumPy.helpers import GetMulti
import os

class NetobjSelector:
    """This class implements a Tkinter widget for a listbox (with scroll bar)
    that contains all instances of a certain network object type and lets the
    user select one or several of those.
    """
    def __init__(self, master, container, displayattrs, resultattr=None, **kwords):
        """The constructor for the widget.

        master - object - the parent widget
        container	- object - the network object container for which the attribute
                             values are retrieved, e.g. Visum.Net.Links
        displayattrs - list(string) - attributes of that network object type which are
                                      to be displayed as the list entry for an object.
                                      A typical choice is the key attribute(s) of the
                                      network object type. Attribute values are separated
                                      by vertical bars.
        resultattr - string - If passed, it contains the ID of the attribute whose value
                              is returned for each selected object. If the parameter is
                              omitted, the object itself is returned instead of an attribute
                              value.
        **kwords	All keyword parameters of Tkinter.Listbox can be used, in particular for setting the selection mode and the size of the list box.
        return value	the object. 
        Example: 
        NetobjSelector(frame, Visum.Net.Blocks, 
                              displayattrs=["ID", "VEHCOMBNAME"],
                              height=5,
                              selectmode=Tk.EXTENDED)
        will insert into frame a listbox with all Block objects. List entries look like
        "17 | Bus" where 17 is the block ID and "Bus" is the name of the vehicle combination.
        Multiple selection is allowed and the selection will be returned as a list of
        Block objects.
        NetobjSelector(frame, Visum.Net.Lines, 
                              displayattrs=["NAME"], 
                              resultattr="NAME", 
                              height=5,
                              selectmode=Tk.SINGLE)
        will insert into frame a listbox with all Line objects. The line name is used as the
        list entry and the selection is also returned as the line name.
        Only single selection is allowed.
        """
        self.fr = Tk.Frame(master)
        scrollbar = Tk.Scrollbar(self.fr)
        scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.LB = Tk.Listbox(self.fr, exportselection=False, **kwords)
        # attach listbox to scrollbar
        self.LB.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.LB.yview)
        dispvals = [ GetMulti(container, attr) for attr in displayattrs ]
        dispvals = zip(*dispvals) # one tuple for each object
        dispvals = [ " | ".join(map(unicode, vals)) for vals in dispvals ] # one string each
        for val in dispvals:
            self.LB.insert(Tk.END, val)
        self.LB.pack(side=Tk.LEFT, fill=Tk.BOTH)

        if resultattr == None:
            self.resultvals = container.GetAll
        else:
            self.resultvals = GetMulti(container, resultattr)

    def getFrame(self):
        """The widget is internally implemented as a Frame containing a Listbox
        and a Scrollbar. getFrame returns the Frame object, in case you want to
        apply any special formatting or layout. Normally not needed.
        """
        return self.fr

    def getListBox(self):
        """The widget is internally implemented as a Frame containing a Listbox
        and a Scrollbar. getListBox returns the list box object, in case you want to
        apply any special formatting or layout. Normally not needed.
        """
        return self.LB

    def getSelection(self):
        """returns the current selection as a list.
        The contents of the list is determined by the value
        of resultattr in the constructor. A single selection
        will be returned as a list of length one."""
        return [ self.resultvals[int(sel)] for sel in self.LB.curselection() ]

    def setSelectionInd(self, newsel):
        """sets the (single) selection to newsel which must be one of the strings in the listbox."""
        for sel in self.LB.curselection():
            self.LB.selection_clear(sel)
        self.LB.selection_set(newsel)

    def grid(self, **kwords):
        self.fr.grid(**kwords)

    def pack(self, **kwords):
        self.fr.pack(**kwords)


class ProgressDlg(Tk.Toplevel):
    """This class implements a progress dialog for tasks that may take a long time.
    It contains a text field for the description of the current acitivity,
    a progress bar and a cancel button. Construct the progress dialog at the
    beginning of a long task, then call repeatedly the setMessage method and
    at the end destroy the dialog. Optionally call isAborted to check whether
    the user has hit the cancel button.
    """
    def __init__(self, title="Progress", **kwparams):
        """The constructor for the dialog.
        
        title	- string - The window title of the progress dialog
        **kwords	All keyword parameters of Tkinter.Toplevel can be used, in particular for setting the size, border and colors of the dialog.
        return - object -	the dialog. 
        """
        self.root = Tk.Tk()
        self.root.withdraw()
        Tk.Toplevel.__init__(self, **kwparams)
        self.createWidgets()
        self.aborted = False
        self.title(title)
        self.percent = 0
        self.lift()
        self.update()

    def close(self):
        self.root.destroy()
        
    def createWidgets(self):
        self.msglabel = Tk.Label(self, text="")
        self.msglabel.pack()
        self.BarCanvas=Tk.Canvas(self,width=300,height=20,bo=1)
        self.BarCanvas.pack(padx=2)
        frame=self.BarCanvas.create_rectangle(0,0,300,20)
        self.BarCanvas.itemconfigure(frame,fill="white")
        self.RectangleID=self.BarCanvas.create_rectangle(0,0,0,20)
        self.BarCanvas.itemconfigure(self.RectangleID,fill="blue")
        self.BarCanvas.coords(self.RectangleID,0,0,0,20)
        Tk.Button(self, text="Cancel", command=self.doAbort).pack()

    def doAbort(self):
        self.aborted = True

    def isAborted(self):
        """Returns a Boolean value. True means that the user has
        hit the cancel button. As a side effect this will close the
        dialog, but all other reactions, like quitting the long task,
        must be programmed individually.
        """
        self.update()
        if self.aborted:
            self.close()
        return self.aborted

    def setMessage(self, msg, progress=0, total = 100):
        """Sets the current progress message in the dialog.

        msg	- string - The text of the message
        progress, total - number -	If progress = x and total = y are passed, it means that the progress is at "x out of y". The progress bar will be drawn accordingly, and the string "(x/y)" is appended to the message text.
        return -	none. 
        """
        if progress > 0:
            msg = "%s (%d/%d)" % (msg, progress, total)
        self.msglabel.config(text=msg)
        progresspixel=float(progress) / total * 300
        self.BarCanvas.coords(self.RectangleID,0,0,progresspixel,20)
        self.update()


def fileChooser(title, fileTypes=[('','*.*')], startDir=os.getcwd()):
    """File chooser dialog
    10/20/07 added dir argument to set directory

    title - string - widget title
    fileTypes - list(tuple) - pairs for file types, see filetypes argument to tkFileDialog
        default fileTypes argument is no file type filter (*.*)
    startDir = string - directory to start the file chooser in

    return - string - filename

    fileChooser("Choose filter file", [('Filter File','.fil')])
    fileChooser("Choose filter file", [('Filter File','.fil')], "C:/project")
    """

    #Start up Tk root
    root = Tk.Tk()
    root.withdraw()

    #Get file name
    fileName = tkFileDialog.askopenfilename(title=title, filetypes=fileTypes, initialdir=startDir, parent=root)

    #Remove root and return filename
    root.destroy()
    return fileName


def messageBox(message, title="Info"):
    """Message box

    message - string - text message
    title - string - widget title, default is "Info"

    return - null - null

    messageBox("Script Complete")
    """

    #Start up Tk root
    root = Tk.Tk()
    root.withdraw()

    #Show info
    tkMessageBox.showinfo(title,message,parent=root)

    #Remove root
    root.destroy()

