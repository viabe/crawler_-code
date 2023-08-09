from PIL import Image
import os
#디렉토리 탐색 알고리즘
for root, dirs, files in os.walk(".\\"):
    height = 0 
    print(root)
    #해당 디렉토리의 모든 파일들을 리턴
    for file in files:
        #해당 파일의 확장자가 png만 처리
        if not file.endswith(".png"):
            continue
        #root는 탐색 디렉토리 file은 파일이름으로 path 해당파일의 전체경로
        path = root + os.sep + file
        img = Image.open(path)
        if img.width != 690:
            continue
        print(path, img.width, img.height)
        height += img.height
    new_height =0
    for file in files:
        if not file.endswith(".png"):
            continue
        path = root + os.sep + file
        img = Image.open(path)
        if img.width != 690:
            continue
        print(path, img.height)
        new_img.paste(path, (0, new_height))