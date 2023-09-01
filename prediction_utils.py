import cv2
import shutil
import os
from ultralytics import YOLO
from PIL import Image

"""
파일 확장자를 체크하는 함수

    : 허용된 확장자인지 아닌지 확인함
"""
def allowed_file(filename):

    # 허용된 확장자 설정
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
이미지를 전처리하는 함수

    : 이미지를 리사이징해서 그 결과 이미지의 경로를 return값으로 받음 
"""
def resize_with_padding(image_path, 
                        save_folder,
                        target_width = 960, 
                        target_height = 540):
    
    img = Image.open(image_path)

    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    # 타겟 크기에 맞게 업스케일 또는 다운스케일 계산
    if aspect_ratio > (target_width / target_height):
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_width = int(target_height * aspect_ratio)
        new_height = target_height

    # 이미지 크기 조정
    resized_img = img.resize((new_width, new_height))

    # 패딩을 추가하기 위해 빈 캔버스 생성
    padded_img = Image.new("RGB", (target_width, target_height))

    # 패딩 계산
    padding_x = (target_width - new_width) // 2
    padding_y = (target_height - new_height) // 2

    # 조정된 이미지를 패딩을 고려하여 중앙에 배치
    padded_img.paste(resized_img, (padding_x, padding_y))

    # 원본 이미지의 파일 이름 추출
    original_image_name = os.path.basename(image_path)
    
    # 원본 이미지랑 동일하게 이름 설정
    new_image_name = f'resize_{original_image_name}'

    # 리사이징한 이미지 저장
    padding_image_path = os.path.join(save_folder, new_image_name)
    padded_img.save(padding_image_path)

    return padding_image_path


"""
모델을 불러오는 함수
"""
def load_yolo_model(model_path = "model/best_1.pt"):
    
    model = YOLO(model_path)
 
    return model


"""
모델을 사용해서 예측하는 함수
    : temps 폴더에 있는 리사이징된 이미지로 예측
      모델이 돌아가고 나면 runs 파일이 생기는데 예측 이미지만 가져오고 runs 파일은 제거함
"""
def predict_image(model, image_path, save_folder):

    # 이미지 읽어오기
    image = cv2.imread(image_path)

    # 예측 
    model.predict(image, save = True)

    # predictions 이미지 경로
    source_image_path = "runs/detect/predict/image0.jpg"
    
    # 리사이징한 이미지의 파일 이름 추출
    image_name = os.path.basename(image_path)
    
    # 새로운 이름 생성 (원본 이미지 이름 앞에 'pred_'를 붙임)
    new_image_name = image_name.replace("resize_", "pred_")
    
    # 새로운 이미지 경로
    predictions = os.path.join(save_folder, new_image_name)

    # 업로드 폴더가 없다면 생성
    os.makedirs(os.path.dirname(predictions), exist_ok=True)
    #os.makedirs(predictions, exist_ok = True) 
        
    # 이미지 이름 변경 및 이동
    os.rename(source_image_path, predictions)
    #shutil.move(source_image_path, predictions)

    # 이동 후에는 디렉토리 삭제
    directory_to_delete = "runs"
    try:
        shutil.rmtree(directory_to_delete)
        print(f"디렉토리 삭제 완료: {directory_to_delete}")
    except Exception as e:
        print(f"디렉토리 삭제 실패: {e}")

    # 확인
    #print(f'destination_image_path : {predictions}')

    return predictions
