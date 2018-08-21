from qtconsole.qt import QtCore, QtGui
import copy

class ParChoiceWidget(QtGui.QWidget):
    '''
    Lets the user select between the pre-fit and post-fit model for the
    loaded pulsar
    '''
    def __init__(self, parent=None, **kwargs):
        super(ParChoiceWidget, self).__init__(parent, **kwargs)

        self.parent = parent
        self.hbox = QtGui.QHBoxLayout()

        self.choose_callback = None
        
        self.initLayout()

    def initLayout(self):
        self.prefit = QtGui.QRadioButton('Pre-Fit')
        self.prefit.toggled.connect(lambda:self.choose(self.prefit))
        self.prefit.setChecked(True)
        self.hbox.addWidget(self.prefit)

        self.postfit = QtGui.QRadioButton('Post-Fit')
        self.postfit.toggled.connect(lambda:self.choose(self.postfit))
        self.hbox.addWidget(self.postfit)
        
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

    def setCallbacks(self, choose):
        self.choose_callback = choose

    def getChoice(self):
        if self.prefit.isChecked():
            return 'prefit'
        else:
            return 'postfit'

    def choose(self, choice):
        if choice.isChecked():
            if self.choose_callback is not None:
                self.choose_callback()
            print(choice.text()) 

class ParEditWidget(QtGui.QWidget):
    '''
    Lets the user edit selected values for the pulsar
    '''
    def __init__(self, parent=None, **kwargs):
        super(ParEditWidget, self).__init__(parent, **kwargs)

        self.parent = parent
        self.layout = QtGui.QVBoxLayout()

        self.table = QtGui.QTableWidget()

        self.initLayout()

    def initLayout(self):
        self.layout.addWidget(self.table)
        self.layout.setStretch(0, 1)

        hbox = QtGui.QHBoxLayout()

        button = QtGui.QPushButton('Add Row')
        button.clicked.connect(self.addRow)
        hbox.addWidget(button)

        button = QtGui.QPushButton('Delete Row')
        button.clicked.connect(self.deleteRow)
        hbox.addWidget(button)

        hbox.addStretch()

        self.layout.addLayout(hbox)
        self.setLayout(self.layout)

    def setCallbacks(self, model):
        self.addTable(model)

    def addTable(self, model):
        '''
        Add the grid of editable boxes for the parfile
        '''
        print('Loading model')
        #Delete old boxes
        self.table.clear()
        self.table.setRowCount(len(model.params))
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels('Parameter;Value;Fit?;Uncertainty;'.split(';'))

        fitpars = [p for p in model.params if not getattr(model, p).frozen]
        
        header = self.table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)

        for ii, par in enumerate(model.params):
            label = QtGui.QTableWidgetItem(par)
            label.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table.setItem(ii, 0, label)

            val = getattr(model, par).value
            vitem = QtGui.QTableWidgetItem(str(val) if val is not None else '')
            self.table.setItem(ii, 1, vitem)
           
            cbox = QtGui.QTableWidgetItem()
            cbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            cbox.setCheckState(QtCore.Qt.Checked if par in fitpars else QtCore.Qt.Unchecked)
            self.table.setItem(ii, 2, cbox)

            uval = getattr(model, par).uncertainty_value
            uitem = QtGui.QTableWidgetItem(str(uval) if uval is not None else '')
            self.table.setItem(ii, 3, uitem)

    def insertRow(self, row):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QtGui.QTableWidgetItem(''))
        self.table.setItem(row, 1, QtGui.QTableWidgetItem(''))
        cbox = QtGui.QTableWidgetItem()
        cbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        cbox.setCheckState(QtCore.Qt.Unchecked)
        self.table.setItem(row, 2, cbox)
        self.table.setItem(row, 3, QtGui.QTableWidgetItem(''))
        

    def addRow(self):
        print('Add Row Clicked')
        indices = []
        for index in self.table.selectionModel().selectedRows():
            indices.append(QtCore.QPersistentModelIndex(index))
        if len(indices) > 0:
            for index in indices:
                self.insertRow(index.row()) 
        else:
            self.insertRow(self.table.rowCount())

    def deleteRow(self):
        print('Delete Row Clicked')
        indices = []
        for index in self.table.selectionModel().selectedRows():
            indices.append(QtCore.QPersistentModelIndex(index))
        for index in indices:
            self.table.removeRow(index.row())

class ParActionsWidget(QtGui.QWidget):
    '''
    Allows the user to reset the model, apply changes, or save to a parfile
    '''
    def __init__(self, parent=None, **kwargs):
        super(ParActionsWidget, self).__init__(parent, **kwargs)
        
        self.parent = parent
        self.hbox = QtGui.QHBoxLayout()
        
        self.reset_callback = None
        self.apply_callback = None
        self.write_callback = None
        
        self.initLayout()

    def initLayout(self):
        button = QtGui.QPushButton('Reset Changes')
        button.clicked.connect(self.resetChanges)
        self.hbox.addWidget(button)

        button = QtGui.QPushButton('Apply Changes')
        button.clicked.connect(self.applyChanges)
        self.hbox.addWidget(button)
        
        button = QtGui.QPushButton('Write Par')
        button.clicked.connect(self.writePar)
        self.hbox.addWidget(button)

        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

    def setCallbacks(self, resetChanges, applyChanges, writePar):
        self.reset_callback = resetChanges
        self.apply_callback = applyChanges
        self.write_callback = writePar

    def resetChanges(self):
        if self.reset_callback is not None:
            self.reset_callback()
        print('Reset clicked')

    def applyChanges(self):
        if self.apply_callback is not None:
            self.apply_callback()
        print('Apply clicked')

    def writePar(self):
        if self.write_callback is not None:
            self.write_callback()
        print('Write clicked')

class ParWidget(QtGui.QWidget):
    '''
    A widget that allows editing and saving of a pulsar parfile
    '''
    def __init__(self, parent=None, **kwargs):
        super(ParWidget, self).__init__(parent, **kwargs)

        self.psr = None

        self.initPar()
        self.initParLayout()
        self.parent = parent
    
    def initPar(self):
        self.layout = QtGui.QVBoxLayout()
        
        self.choiceWidget = ParChoiceWidget(parent=self)
        self.editWidget = ParEditWidget(parent=self)
        self.actionsWidget = ParActionsWidget(parent=self)

    def initParLayout(self):
        self.layout.addWidget(self.choiceWidget)
        self.layout.addWidget(self.editWidget)
        self.layout.setStretch(1, 1)
        self.layout.addWidget(self.actionsWidget)
        
        self.setLayout(self.layout)

    def setPulsar(self, psr):
        self.psr = psr

        self.choiceWidget.setCallbacks(self.set_model)
        self.editWidget.setCallbacks(self.psr._model)
        self.actionsWidget.setCallbacks(self.set_model, 
                                        self.applyChanges, 
                                        self.writePar)

    def set_model(self):
        choice = self.choiceWidget.getChoice()
        if choice == 'postfit':
            self.editWidget.setCallbacks(self.psr._fitter.model)
        elif choice == 'prefit':
            self.editWidget.setCallbacks(self.psr._model)

    def updateModel(self, model, table):
        for xx in range(table.rowCount()):
            par = table.item(xx, 0).text()
            val = table.item(xx, 1).text()
            fit = table.item(xx, 2).checkState()
            fit = True if fit == QtCore.Qt.Checked else False
            unc = table.item(xx, 3).text()
            #Edit existing row
            if hasattr(model, par):
                if not val == '':
                    try:
                        val = float(val)
                    except:
                        if val == 'True':
                            val = True
                        elif val == 'False':
                            val = False
                        else:
                            print('%s cannot resolve value %s' % (par, val))
                    getattr(model, par).value = val
                getattr(model, par).frozen = not fit 
                if not unc == '':
                    try:
                        unc = float(unc)
                        getattr(model, par).uncertainty_value = unc
                    except:
                        print('%s uncertainty value %s could not be set' % (par, unc))
                print(par, val, fit, unc)

    def applyChanges(self):
        self.updateModel(self.psr._model, self.editWidget.table)

    def writePar(self):
        model = copy.deepcopy(self.psr._model)
        self.updateModel(model, self.editWidget.table)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Choose output par file', '~/')
        fout = open(filename, 'w')
        fout.write(model.as_parfile())
        fout.close()
        print('Saved edited parfile to %s' % filename)


