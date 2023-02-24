import numpy as np
import openpyxl
import time, os
import pandas as pd
import os
import time
import pandas as pd

from pandas import ExcelWriter

lista = []
listb = []

File_data = np.loadtxt("data.txt", dtype=int)


def get_array(datarry):
    list_tmp = []
    for x in datarry[0]:
        for y in datarry[1]:
            for z in datarry[2]:
                list_tmp.append(str(x) + str(y) + str(z))
    return list_tmp


def write_sheet(data, writ, sheetname):
    df = pd.DataFrame(data)
    df.to_excel(writ, sheet_name=sheetname)

    # df1 = pd.DataFrame({'Data': ['a', 'b', 'c', 'd']})
    # df1.to_excel(writer, sheet_name='Sheeta')


lista = get_array(File_data[0:3])
listb = get_array(File_data[3:6])
#
# print(lista)
# print(listb)
# print("a-b")
# print(np.setdiff1d(lista, listb, True))
# print("b-a")
# print(np.setdiff1d(listb, lista, True))
# print("a+b")
# print(np.union1d(lista, listb))
# print("ab只出现过一次")
# print(np.setxor1d(lista, listb))
# print("ab的交集")
# print(np.intersect1d(lista, listb))

writer = pd.ExcelWriter('multiple'+time.strftime('%Y%m%d%H%M%S', time.localtime()) +'.xlsx', engine='openpyxl')

write_sheet(lista, writer, "a")
write_sheet(listb, writer, "b")
write_sheet(np.setdiff1d(lista, listb, True), writer, "a-b")
write_sheet(np.setdiff1d(listb, lista, True), writer, "b-a")
write_sheet(np.union1d(lista, listb), writer, "a+b")
write_sheet(np.intersect1d(lista, listb), writer, "ab的交集")

writer.save()
