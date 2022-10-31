Sub add_Picture()
    Dim picname As String
    Dim pasteAt As Integer
    Dim lThisRow As Long
    lThisRow = 2 'This is the start row
    Do While(Cells(lThisRow, 4) <> "") ' 4,本地文件名相关列
        pasteAt = lThisRow
        picname = Cells(lThisRow, 4) 'This is the picture name
        present = Dir("D:\workspaces\mailipy-master\qrimg\" & picname & "_qr.png")
        If present <> "" Then
            Cells(pasteAt, 7) = "D:\workspaces\mailipy-master\qrimg\" & picname & "_qr.png" '这一列放生成的文件名，做参考
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


