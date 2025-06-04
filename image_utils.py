import os
import base64
import cv2

def extract_frames(video_path, output_folder, frame_interval_sec=3):
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps * frame_interval_sec)

    frame_count = 0
    saved = 0

    while cap.isOpened():
        
        ret, frame = cap.read()
        if not ret:
            break
        if saved == 10:
            break
        if frame_count % interval == 0:

            filename = os.path.join(output_folder, f"frame_{saved}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1

        frame_count += 1
    
    cap.release()
    return saved

def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_encoded_frames(frame_dir, max_frames=10):
    
    image_blocks = []

    for i in range(max_frames):
        
        frame_path = os.path.join(frame_dir, f"frame_{i}.jpg")
        
        if not os.path.exists(frame_path):
            break
        image_blocks.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": encode_image_base64(frame_path)
            }
        })

    return image_blocks