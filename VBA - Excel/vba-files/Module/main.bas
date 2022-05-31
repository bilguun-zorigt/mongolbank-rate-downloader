Attribute VB_Name = "main"
Option Explicit

Sub parse(ResponseText, DateSerialValue)
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
            Call Rates.add(DateSerialValue, Symbol, Rate)
        End If
    Next Element

End Sub


Sub request(myURL, DateSerialValue)
    'Make async for speed
    'https://stackoverflow.com/questions/11431677/how-to-vba-sends-an-async-xmlhttp-request
    'https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms757849(v=vs.85)
    'https://stackoverflow.com/questions/9866930/can-i-do-an-async-xml-call-in-excel-2010-vba
    'http://dailydoseofexcel.com/archives/2006/10/09/async-xmlhttp-calls/
    Dim HttpRequest As Object
    Set HttpRequest = CreateObject("MSXML2.XMLHTTP.6.0")
    HttpRequest.Open "GET", myURL, False '<= True Async, False Sync
    HttpRequest.send
    If HttpRequest.Status = 200 Then Call parse(HttpRequest.ResponseText, DateSerialValue)
End Sub

Sub main()
    Dim myURL As String
    Dim DateSerialValue As Date
    Dim start_date_string As Variant
    Dim end_date_string As Variant
    Dim start_date As Date
    Dim end_date As Date
    start_date_string = Split(Application.InputBox("Enter start date (yyyy-mm-dd): "), "-")
    end_date_string = Split(Application.InputBox("Enter end date (yyyy-mm-dd): "), "-")
    start_date = DateSerial(start_date_string(0), start_date_string(1), start_date_string(2))
    end_date = DateSerial(end_date_string(0), end_date_string(1), end_date_string(2))
    For DateSerialValue = start_date To end_date
        myURL = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=" & Year(DateSerialValue) & "&vMonth=" & month(DateSerialValue) & "&vDay=" & Day(DateSerialValue)
        Call request(myURL, CLng(DateSerialValue))
    Next DateSerialValue
End Sub

