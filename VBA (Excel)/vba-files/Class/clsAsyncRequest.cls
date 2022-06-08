VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsAsyncRequest"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Public xml_http_request As Object
Private date_sn As Date

Property Let DateSN(DateSN As Date)
date_sn = DateSN
Dim URL As String
URL = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear=" & Year(DateSN) & "&vMonth=" & month(DateSN) & "&vDay=" & Day(DateSN)
Set xml_http_request = CreateObject("MSXML2.XMLHTTP.6.0") 'New MSXML2.XMLHTTP
xml_http_request.OnReadyStateChange = Me
xml_http_request.Open "GET", URL, True
xml_http_request.send
End Property


Sub OnReadyStateChange()
Attribute OnReadyStateChange.VB_UserMemId = 0
    If xml_http_request.readyState = 4 Then
        If xml_http_request.Status = 200 Then
            ' MsgBox xml_http_request.ResponseText
            Call parse(xml_http_request.ResponseText, date_sn)
        Else
            'Error happened
        End If
    End If
End Sub
