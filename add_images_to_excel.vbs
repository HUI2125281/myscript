Sub Picture()
    Dim picname As String
    Dim shp As Shape
    Dim pasteAt As Integer
    Dim lThisRow As Long
    lThisRow = 2 'This is the start row
    Do While(Cells(lThisRow, 4) <> "")
        pasteAt = lThisRow
        picname = Cells(lThisRow, 4) 'This is the picture name
        present = Dir("D:\workspaces\mailipy-master\qrimg\" & picname & "_qr.png")
        Cells(pasteAt, 7) = "D:\workspaces\mailipy-master\qrimg\" & picname & "_qr.png"
        If present <> "" Then
            Set Rng = Cells(pasteAt, 6)
            Set sShape = ActiveSheet.Shapes.AddPicture("D:\workspaces\mailipy-master\qrimg\" & picname & "_qr.png", msoFalse, msoCTrue, Rng.Left, Rng.Top, Rng.Width, Rng.Height)
        Else
            Cells(pasteAt, 6) = "No Picture Found"
        End If
        lThisRow = lThisRow + 1
    Loop
    Range("A1").Select
    Application.ScreenUpdating = True
    Exit Sub
    ErrNoPhoto
    MsgBox "Unable to Find Photo" 'Shows message box if picture not found
    Exit Sub
End Sub


