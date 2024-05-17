import pyrealsense2 as rs
import numpy as np
import cv2
import time

def draw_countdown(frame, seconds_left):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 6
    font_thickness = 5
    text_color = (255, 255, 255)  # 白色
    text = str(seconds_left)
    text_size = cv2.getTextSize(text, font, font_size, font_thickness)[0]
    text_position = ((frame.shape[1] - text_size[0]) // 2, (frame.shape[0] + text_size[1]) // 2)
    cv2.putText(frame, text, text_position, font, font_size, text_color, font_thickness, cv2.LINE_AA)

def show_frame_in_window(frame):
    cv2.imshow('Camera Feed', frame)
    cv2.waitKey(1)

def record_delayed_video_with_countdown(output_folder, delay=3, duration=6):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

    for remaining_seconds in range(int(delay), 0, -1):
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        frame = np.asanyarray(color_frame.get_data())
        draw_countdown(frame, remaining_seconds)
        show_frame_in_window(frame)
        time.sleep(1)

    fps = 30
    width = 640
    height = 480
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    current_time = time.strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_folder}/{current_time}.avi"
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    start_time = time.time()

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        frame = np.asanyarray(color_frame.get_data())

        out.write(frame)
        show_frame_in_window(frame)

        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

    pipeline.stop()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    output_folder = "test"
    record_delayed_video_with_countdown(output_folder, delay=3, duration=6)
