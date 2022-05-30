Attribute VB_Name = "main"
Option Explicit

Sub DownloadFile()

    Dim myURL As String
    myURL = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=2022&vMonth=2&vDay=7"

    Dim HttpRequest As Object
    Dim HTML As Object
    Dim Elements As Object
    dim Element As Object

    Set HttpRequest = CreateObject("MSXML2.XMLHTTP.6.0")
    HttpRequest.Open "GET", myURL, False '<= True Async

    'Make async for speed
    'https://stackoverflow.com/questions/11431677/how-to-vba-sends-an-async-xmlhttp-request
    'https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms757849(v=vs.85)
    'https://stackoverflow.com/questions/9866930/can-i-do-an-async-xml-call-in-excel-2010-vba
    'http://dailydoseofexcel.com/archives/2006/10/09/async-xmlhttp-calls/

    HttpRequest.send

    If HttpRequest.Status = 200 Then
        Set HTML = CreateObject("htmlfile")
        HTML.body.innerhtml = HttpRequest.responsetext
        Set Elements = HTML.getelementbyid("ContentPlaceHolder1_panelExchange").getElementsByTagName("span")
        debug.Print("***Start***")
        For Each Element In Elements
            Debug.Print Element.ID & " : " & Element.innerText
        Next Element
        debug.Print("***End***")
    End If

End Sub

