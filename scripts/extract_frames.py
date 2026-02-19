import os
import sys
from pathlib import Path

import cv2

# 預設輸出目錄
OUTPUT_DIR = "frames"


def _ensure_output_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def extract_frames(video_path, output_dir=OUTPUT_DIR, interval=5):
    """從影片提取識別幀與掃描幀。"""
    if interval <= 0:
        raise ValueError("interval 必須大於 0")

    if not os.path.isfile(video_path):
        print(f"錯誤: 找不到影片檔案 {video_path}")
        return False

    _ensure_output_dir(output_dir)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"錯誤: 無法開啟影片檔案 {video_path}")
        return False

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if fps <= 0:
            print("錯誤: FPS 無效 (<= 0)")
            return False

        duration = total_frames / fps
        print(f"影片 FPS: {fps}, 長度: {duration:.2f}秒")

        # 1. 識別幀 (約 20 秒處 - 通常載入畫面已結束)
        # 嘗試抓取早期幀數以獲取帶有名字的 HUD 介面
        for t in [20, 60]:
            if t < duration:
                cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
                ret, frame = cap.read()
                if ret:
                    filename = os.path.join(output_dir, f"ident_{t}s.jpg")
                    cv2.imwrite(filename, frame)
                    print(f"已儲存識別幀: {filename}")

        # 2. 掃描幀 (每 interval 秒一張)
        current_time = 0
        failed_reads = 0

        while current_time < duration:
            cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
            ret, frame = cap.read()
            if not ret:
                # 某些編碼在特定時間戳會 seek/read 失敗，跳過該時間點繼續提取
                failed_reads += 1
                current_time += interval
                continue

            mins = int(current_time // 60)
            secs = int(current_time % 60)
            filename = os.path.join(output_dir, f"scan_{mins:02d}_{secs:02d}.jpg")
            cv2.imwrite(filename, frame)

            current_time += interval

        if failed_reads:
            print(f"警告: 有 {failed_reads} 個時間點讀取失敗，已自動略過。")

        print("幀提取完成。")
        return True
    finally:
        cap.release()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_frames.py <影片檔案路徑>")
        sys.exit(1)

    video_file = sys.argv[1]
    success = extract_frames(video_file)
    sys.exit(0 if success else 2)
