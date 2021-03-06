import os
import sys
import bz2
from tensorflow.keras.utils import get_file
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector

class images_align_tool:
    LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
    
    def initTool(self):
        self.landmarks_model_path = self._unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
                                                         images_align_tool.LANDMARKS_MODEL_URL, cache_subdir='temp'))
        print(self.landmarks_model_path)
    
    def _unpack_bz2(self, src_path):
        data = bz2.BZ2File(src_path).read()
        dst_path = src_path[:-4]
        with open(dst_path, 'wb') as fp:
            fp.write(data)
        return dst_path


    def align(self, raw_img_dir, aligned_img_dir):
        RAW_IMAGES_DIR = raw_img_dir
        ALIGNED_IMAGES_DIR = aligned_img_dir

        landmarks_detector = LandmarksDetector(self.landmarks_model_path)
        for img_name in os.listdir(RAW_IMAGES_DIR):
            raw_img_path = os.path.join(RAW_IMAGES_DIR, img_name)
            for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
                face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], i)
                aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)

                image_align(raw_img_path, aligned_face_path, face_landmarks)
