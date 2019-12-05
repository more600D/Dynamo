Function GreedyAlgo&(dl As Range, klv As Range, sm&, Optional shrez& = 0, Optional krm& = 0) 'жадный алгоритм
    Dim i&, j&, k&, l&, t&, s&, aArr&(), bArr() As Boolean, bFlag As Boolean
    
    For i = 1 To dl.Count 'ввод исходных данных
        If Val(dl(i)) > 0 Then
            For j = 1 To Val(klv(i))
                k = k + 1
                ReDim Preserve aArr&(1 To k), bArr(1 To k) As Boolean
                aArr(k) = Val(dl(i)) + shrez
            Next j
        End If
    Next i
        
    For i = 1 To k 'сортировка пузырьков
        For j = 1 To i - 1
            If aArr(i) > aArr(j) Then t = aArr(i): aArr(i) = aArr(j): aArr(j) = t
    Next j, i
       
    Do 'определяем кол-во
        s = sm - krm
        bFlag = False
        l = l + 1
        For i = 1 To k
            If s >= aArr(i) And Not bArr(i) Then
                s = s - aArr(i)
                bArr(i) = True
                bFlag = True
            End If
        Next i
    Loop While bFlag And s < sm - krm
    GreedyAlgo = l - 1
End Function