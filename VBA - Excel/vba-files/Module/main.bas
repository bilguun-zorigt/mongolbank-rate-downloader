Attribute VB_Name = "main"
Option Explicit

Sub DownloadFile()

    Dim myURL As String
    myURL = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=2022&vMonth=2&vDay=7"

    Dim HttpRequest As Object
    Dim HTML As Object
    Dim Spans As Object
    dim Span As Object

    Set HttpRequest = CreateObject("MSXML2.XMLHTTP.6.0")
    HttpRequest.Open "GET", myURL, True
    HttpRequest.send

    If HttpRequest.Status = 200 Then
        Set HTML = CreateObject("htmlfile")
        HTML.body.innerhtml = HttpRequest.responsetext
        Set Spans = HTML.getelementbyid("ContentPlaceHolder1_panelExchange").getElementsByTagName("span")
        debug.Print("***Start***")
        For Each Span In Spans
            Debug.Print Span.ID & " : " & Span.innerText
        Next Span
        debug.Print("***End***")
    End If

End Sub

