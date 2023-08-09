from PIL import Image
import os
# 디렉토리 탐색 알고리즘
for root, dirs, files in os.walk(".\\"):
    height = 0
    img_list = []
    # 해당 디렉토리의 모든 파일들을 리턴
    for file in files:
        # 해당 파일의 확장자가 png 만 처리
        if not file.endswith(".png"):
            continue
        # root 는 탐색 디렉토리 file 은 파일이름으로 path 해당파일의 전체경로
        path = root + os.sep + file
        print(path)
        # 해당 이미지파일의 객체를 Image 클래스로 생성
        img = Image.open(path)
        # 웹툰의 가로사이즈가 690 이 아닌 썸네일일 경우 무시
        if img.width != 690:
            continue
        # 이미지리스트안에 해당 이미지 객체를 담는다        
        img_list.append(img)
        # 또한 이미지 파일들의 높이를 계속 더해 전체 높이를 통해 새 이미지파일을 생성하고자 한다
        height += img.height
    # 새 이미지 파일을 생성하기 위해 각각의 이미지파일의 높이를 계산하기 위한 new_height 변수 초기화
    new_height = 0
    # 새로운 이미지 파일을 생성, 가로는 690으로 고정 높이는 이전에 구한 png 파일들의 전체 높이를 더한값
    new_img = Image.new("RGB", (690, height), (256,256,256))
    # 각각의 이미지파일을 반복문으로 진행
    for img in img_list:
        # 각각의 이미지파일을 paste 붙여넣는데 그 위치는 0에서부터 각 png 파일들의 높이를 더한 offset 결정된다
        new_img.paste(img, box = (0, new_height))
        # 각 png 파일들을 더한 offset 을 계산하기 위해 이미지파일의 높이를 더한다
        new_height += img.height
    if root[2:] == "":
        continue    
    # 이미지 파일저장
    new_img.save(root[2:] + ".png")
    new_img.close()
    print("Save Finish", root[2:] + ".png")
    