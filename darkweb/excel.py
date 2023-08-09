# 엑셀 모듈을 로드
import openpyxl

'''
# 엑셀 파일을 선언
book = openpyxl.Workbook()
# 새 시트를 선언
sheet = book.active
# 시트에 데이터 담기
sheet.append([1,2,3,4,5])
sheet.append(["1231231",2,"3",4,5])
# 엑셀 파일저장
book.save("kisia.xlsx")
book.close()
'''
# kisia.xlsx 파일을 로드
book = openpyxl.load_workbook("kisia.xlsx")
sheet = book.worksheets[0]
for row in sheet.rows:
    for i in range(len(row)):
        print(row[i].value, end=" ")
    print()
    
    