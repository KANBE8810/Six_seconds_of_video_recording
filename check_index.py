
import cv2

def detect_camera_indexes():
    # カメラデバイスの数を取得
    num_devices = 10  # 最大10個までチェックする

    # 利用可能なカメラデバイスのリストを格納するリスト
    available_cameras = []

    # カメラデバイスのインデックスをチェック
    for index in range(num_devices):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()

    return available_cameras

if __name__ == "__main__":
    available_cameras = detect_camera_indexes()
    print("Available camera devices:", available_cameras)
