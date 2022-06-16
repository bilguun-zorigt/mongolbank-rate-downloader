Attribute VB_Name = "main"
Option Explicit

Sub main()
    Dim date_from As Date: date_from = get_date_input("Source code at: https://github.com/bilguun-zorigt" & vbNewLine & vbNewLine & "Enter start date (yyyy-mm-dd): ")
    Dim date_to As Date: date_to = get_date_input("Source code at: https://github.com/bilguun-zorigt" & vbNewLine & vbNewLine & "Enter end date (yyyy-mm-dd): ")

    Dim AsyncRequest As clsAsyncRequest
    Dim DateSN As Date
    For DateSN = date_from To date_to
        Set AsyncRequest = New clsAsyncRequest
        AsyncRequest.DateSN = DateSN
        Next
End Sub


Sub parse(ResponseText, DateSN)
    Dim HTML As Object
    Dim Elements As Object
    Dim Element As Object
    Dim Symbol As String
    Dim Rate As Double

    Set HTML = CreateObject("htmlfile")
    HTML.body.innerhtml = ResponseText
    Set Elements = HTML.getelementbyid("ContentPlaceHolder1_panelExchange").getElementsByTagName("span")

    For Each Element In Elements
        Symbol = Application.Substitute(Element.id, "ContentPlaceHolder1_lbl", "")
        If Symbol <> "Date" Then
            Rate = CDbl(Application.Substitute(Element.innerText, ",", ""))
            Call Rates.add(CLng(DateSN), Symbol, Rate)
        End If
    Next Element

End Sub

Function get_date_input(message As String) As Date
    Dim date_string As Variant
    date_string = Split(Application.InputBox(message), "-")
    get_date_input = DateSerial(date_string(0), date_string(1), date_string(2))
End Function

