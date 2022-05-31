VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Rates"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True

Option Explicit

Private Function get_column(header_name) As Range
    Dim usedrange_header_row As Range
    Dim column_index As Variant
    Set usedrange_header_row = Me.Range("$A$1", Me.Cells.SpecialCells(xlLastCell)).Rows(1)
    column_index = Application.Match(header_name, usedrange_header_row, 0)
    Dim is_empty_sheet As Boolean
    is_empty_sheet = Me.Cells.SpecialCells(xlLastCell).Address = "$A$1" And Me.Range("$A$1") = ""
    If IsError(column_index) Then
        Set get_column = Me.Columns(usedrange_header_row.Columns.Count + IIf(is_empty_sheet, 0, 1))
        get_column.Rows(1).Value2 = header_name
    Else
        Set get_column = Me.Columns(column_index)
    End If
End Function

Private Function get_row(id_column_index, id_name) As Range
    Dim usedrange_id_column As Range
    Dim row_index As Variant
    Set usedrange_id_column = Me.Range("A1", Me.Cells.SpecialCells(xlLastCell)).Columns(id_column_index)
    row_index = Application.Match(id_name, usedrange_id_column, 0)
    If IsError(row_index) Then
        Set get_row = Me.Rows(usedrange_id_column.Rows.Count + 1)
        get_row.Columns(id_column_index).Value2 = id_name
    Else
        Set get_row = Me.Rows(row_index)
    End If
End Function

Sub add(DateSerialValue, Symbol, Rate)
    Dim date_column As Range
    Dim symbol_column As Range
    Dim date_row As Range
    Set date_column = get_column("Date")
    Set symbol_column = get_column(Symbol)
    Set date_row = get_row(date_column.Column, DateSerialValue)
    Intersect(date_row, symbol_column).Value2 = Rate
End Sub
