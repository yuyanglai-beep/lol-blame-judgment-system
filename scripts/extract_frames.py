import argparse
import os
import sys
from pathlib import Path

# 預設輸出目錄
OUTPUT_DIR = "frames"


def _ensure_output_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def _load_cv2():
    """延遲載入 cv2，避免缺依賴時無法輸出友善錯誤。"""
    try:
        import cv2  # type: ignore

        return cv2
    except ModuleNotFoundError:
        print("錯誤: 缺少依賴 opencv-python (cv2)。請先執行: pip install opencv-python")
        return None


def extract_frames(video_path, output_dir=OUTPUT_DIR, interval=5, strict_read_fail=False):
    """從影片提取識別幀與掃描幀。"""
    if interval <= 0:
        print("錯誤: interval 必須大於 0")
        return False

    if not os.path.isfile(video_path):
        print(f"錯誤: 找不到影片檔案 {video_path}")
        return False

    cv2 = _load_cv2()
    if cv2 is None:
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
            if strict_read_fail:
                print("錯誤: strict_read_fail 模式啟用，將此情況視為失敗。")
                return False

        print("幀提取完成。")
        return True
    finally:
        cap.release()


def _build_parser():
    parser = argparse.ArgumentParser(description="LoL 重播幀提取工具")
    parser.add_argument("video_path", help="影片檔案路徑")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="輸出資料夾，預設為 frames")
    parser.add_argument("--interval", type=int, default=5, help="掃描幀間隔（秒），預設為 5")
    parser.add_argument(
        "--strict-read-fail",
        action="store_true",
        help="若任一時間點讀取失敗則回傳失敗",
    )
    return parser


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    success = extract_frames(
        video_path=args.video_path,
        output_dir=args.output_dir,
        interval=args.interval,
        strict_read_fail=args.strict_read_fail,
    )
    sys.exit(0 if success else 2)
