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

Private Function get_row(id_name) As Variant
    Dim usedrange_id_column As Range
    Set usedrange_id_column = Me.Range("$A$1", Me.Cells.SpecialCells(xlLastCell)).Columns(1)
    get_row = Application.Match(id_name, usedrange_id_column, 0)
    If IsError(get_row) Then
        get_row = usedrange_id_column.Rows.Count + 1
        Me.Cells(get_row, 1).Value2 = id_name
    End If
End Function

Private Function get_column(header_name) As Variant
    Dim usedrange_header_row As Range
    Set usedrange_header_row = Me.Range("$A$1", Me.Cells.SpecialCells(xlLastCell)).Rows(1)
    get_column = Application.Match(header_name, usedrange_header_row, 0)
    Dim is_empty_sheet As Boolean
    is_empty_sheet = Me.Cells.SpecialCells(xlLastCell).Address = "$A$1" And Me.Range("$A$1") = ""
    If IsError(get_column) Then
        get_column = usedrange_header_row.Columns.Count + IIf(is_empty_sheet, 0, 1)
        Me.Cells(1, get_column).Value2 = header_name
    End If
End Function

Sub add(DateSN, Symbol, Rate)
    Dim date_row As Long: date_row = get_row(DateSN)
    Dim symbol_column As Long: symbol_column = get_column(Symbol)
    Me.Cells(date_row, symbol_column).Value2 = Rate
End Sub
