import cv2
import time

def draw_countdown(frame, seconds_left):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 6
    font_thickness = 5
    text_color = (255, 255, 255)  # 白色

    # カウントダウンのテキストを描画
    text = str(seconds_left)
    text_size = cv2.getTextSize(text, font, font_size, font_thickness)[0]
    text_position = ((frame.shape[1] - text_size[0]) // 2, (frame.shape[0] + text_size[1]) // 2)
    cv2.putText(frame, text, text_position, font, font_size, text_color, font_thickness, cv2.LINE_AA)

def show_frame_in_window(frame):
    cv2.imshow('Camera Feed', frame)
    cv2.waitKey(1)

def record_delayed_video_with_countdown(output_folder, delay=3, duration=6):
    # カメラのキャプチャを開始（USB接続されたカメラを選択するために引数を変更）
    cap = cv2.VideoCapture(2)  # カメラデバイスのインデックスを指定する

    # カメラ画像を表示（オプション）
    cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

    # 遅延をかけてカメラ画像を表示
    for remaining_seconds in range(int(delay), 0, -1):
        ret, frame = cap.read()
        if not ret:
            break
        draw_countdown(frame, remaining_seconds)
        show_frame_in_window(frame)
        time.sleep(1)

    # カメラ画像表示のウィンドウを閉じる
    cv2.destroyWindow('Camera Feed')

    # 動画の設定
    fps = 60  # フレームレート
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_folder}/{current_time}.avi"

    # 出力動画ファイルの設定
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 開始時刻を取得
    start_time = time.time()

    # カメラ画像を取得して動画に書き込む
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        show_frame_in_window(frame)

        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

    # ビデオを解放してウィンドウを閉じる
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    output_folder = "test"  # 出力動画のフォルダパス
    record_delayed_video_with_countdown(output_folder, delay=3, duration=6)
