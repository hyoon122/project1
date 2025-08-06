# 자동 폴더 분류 스크립트

import os, json, shutil

image_dir = './VS_calib_K_가시광이미지_image_F'
label_dir = './VL_calib_K_가시광이미지_image_F'
output_dir = './data'

os.makedirs(f'{output_dir}/normal', exist_ok=True)
os.makedirs(f'{output_dir}/construction', exist_ok=True)

for label_file in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_file)
    with open(label_path, 'r') as f:
        label = json.load(f)

    image_name = label_file.replace('.json', '.jpg')
    image_path = os.path.join(image_dir, image_name)

    if not os.path.exists(image_path):
        continue

    # 공사 관련 객체 있는지 확인
    has_construction = any(
        'construction' in obj['class'].lower() or
        'barrier' in obj['class'].lower() or
        'cone' in obj['class'].lower()
        for obj in label.get('objects', [])
    )

    dst_dir = 'construction' if has_construction else 'normal'
    shutil.copy(image_path, f'{output_dir}/{dst_dir}/{image_name}')
