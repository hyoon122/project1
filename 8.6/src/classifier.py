import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

# 설정값들
CATEGORIES = ['normal', 'construction']  # 분류할 두 개의 카테고리
DATASET_PATH = './data'  # 이미지가 저장된 최상위 디렉토리
DICTIONARY_SIZE = 50     # BOW 시각 사전의 클러스터 개수 (즉, 단어 수)
MODEL_PATH = './models/bow_svm.pkl'  # 학습된 모델 저장 경로

# 지정된 폴더에서 모든 이미지를 불러오는 함수
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # 이미지는 흑백으로 로드
        if img is not None:
            images.append(img)
    return images

# SIFT 특징점 추출 함수
def extract_sift_features(images, detector):
    descriptors = []
    for img in images:
        keypoints, des = detector.detectAndCompute(img, None)  # 키포인트와 디스크립터 추출
        if des is not None:
            descriptors.extend(des)  # 디스크립터 리스트에 추가
    return descriptors

# 시각 단어 사전(Vocabulary) 생성 함수
def create_bow_dictionary():
    detector = cv2.SIFT_create()  # SIFT 추출기 생성
    bow_trainer = cv2.BOWKMeansTrainer(DICTIONARY_SIZE)  # KMeans 기반 BOW 트레이너

    # 각 카테고리별 이미지에서 SIFT 특징 추출하여 사전 학습
    for category in CATEGORIES:
        path = os.path.join(DATASET_PATH, category)
        images = load_images_from_folder(path)
        descriptors = extract_sift_features(images, detector)
        for des in descriptors:
            bow_trainer.add(np.array([des]))  # BOW 트레이너에 디스크립터 추가

    dictionary = bow_trainer.cluster()  # KMeans로 클러스터링 → 시각 단어 사전 완성
    np.save('./models/dictionary.npy', dictionary)  # 시각 사전 저장 (재사용 가능)
    return dictionary

# 이미지 리스트를 BOW 벡터로 변환하는 함수
def extract_bow_features(images, bow_extractor):
    features = []
    for img in images:
        keypoints = bow_extractor.descriptorExtractor.detect(img, None)  # 키포인트 추출
        bow_feature = bow_extractor.compute(img, keypoints)  # BOW 히스토그램 생성
        if bow_feature is not None:
            features.append(bow_feature.flatten())  # 벡터로 변환 후 리스트에 추가
    return features


