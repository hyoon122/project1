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

