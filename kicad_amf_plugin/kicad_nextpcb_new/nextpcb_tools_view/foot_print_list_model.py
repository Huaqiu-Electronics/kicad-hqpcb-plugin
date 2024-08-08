import sys
import wx
import wx.dataview as dv

#----------------------------------------------------------------------

# This model class provides the data to the view when it is asked for.
# Since it is a list-only model (no hierarchical data) then it is able
# to be referenced by row rather than by item object, so in this way
# it is easier to comprehend and use than other model types.  In this
# example we also provide a Compare function to assist with sorting of
# items in our model.  Notice that the data items in the data model
# object don't ever change position due to a sort or column
# reordering.  The view manages all of that and maps view rows and
# columns to the model's rows and columns as needed.
#
# For this example our data is stored in a simple list of lists.  In
# real life you can use whatever you want or need to hold your data.
MAX_COLS = 14

class FootprintListModel(dv.DataViewIndexListModel):
    def __init__(self, data ):
        # dv.DataViewIndexListModel.__init__(self, len(data))
            # 尝试初始化基类
            dv.DataViewIndexListModel.__init__(self, len(data))
            # super(FootprintListModel, self).__init__(len(data))
            self.data = data

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):

        if col < 0 or col >= MAX_COLS:
            return None 
        return self.data[row][col]
    
    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        if 0 <= col < len(self.data[row]):
            self.data[row][col] = value
            return True
        return False

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return MAX_COLS  

    # Specify the data type for a column
    def GetColumnType(self, col):
        return "string"  

    # Report the number of rows in the model
    def GetCount(self):
        #self.log.write('GetCount')
        return len(self.data)


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0:
            return (self.data[row1][0] > self.data[row2][0]) - (self.data[row1][0] < self.data[row2][0]) if ascending else -1 * ((self.data[row1][0] > self.data[row2][0]) - (self.data[row1][0] < self.data[row2][0]))
        else:
            return 0
        
    def DeleteRows(self, rows):
        for row in sorted(rows, reverse=True):
            del self.data[row]
        self.RowDeleted(row)


    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()

