import cv2
import os
import sys

# 預設輸出目錄
OUTPUT_DIR = "frames"

def extract_frames(video_path):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"錯誤: 無法開啟影片檔案 {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if fps == 0:
        print("錯誤: FPS 為 0")
        return

    duration = total_frames / fps

    print(f"影片 FPS: {fps}, 長度: {duration:.2f}秒")

    # 1. 識別幀 (約 20 秒處 - 通常載入畫面已結束)
    # 嘗試抓取早期幀數以獲取帶有名字的 HUD 介面
    for t in [20, 60]:
        if t < duration:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = cap.read()
            if ret:
                filename = os.path.join(OUTPUT_DIR, f"ident_{t}s.jpg")
                cv2.imwrite(filename, frame)
                print(f"已儲存識別幀: {filename}")

    # 2. 掃描幀 (每 5 秒一張)
    interval = 5  # 秒
    current_time = 0
    
    while current_time < duration:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, frame = cap.read()
        if not ret:
            break
        
        # 儲存幀
        mins = int(current_time // 60)
        secs = int(current_time % 60)
        # 格式: scan_分_秒.jpg
        filename = os.path.join(OUTPUT_DIR, f"scan_{mins:02d}_{secs:02d}.jpg")
        cv2.imwrite(filename, frame)
        
        current_time += interval

    cap.release()
    print("幀提取完成。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_frames.py <影片檔案路徑>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    extract_frames(video_file)
