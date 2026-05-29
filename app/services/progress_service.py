from tqdm import tqdm
import time

# --------------------------------------------------
# Progress Manager
# --------------------------------------------------

class ProgressManager:

    def __init__(self):

        self.progress_bar = tqdm(
            total=100,
            desc="Meeting AI Processing",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
        )

        self.current_progress = 0

    # --------------------------------------------------
    # progress 업데이트
    # --------------------------------------------------

    def update(self, target_progress, message):

        increment = target_progress - self.current_progress

        if increment > 0:
            self.progress_bar.update(increment)

        self.current_progress = target_progress

        self.progress_bar.set_description(message)

        print(f"\n[{target_progress}%] {message}")

    # --------------------------------------------------
    # 종료
    # --------------------------------------------------

    def finish(self):

        remaining = 100 - self.current_progress

        if remaining > 0:
            self.progress_bar.update(remaining)

        self.progress_bar.set_description(
            "Completed"
        )

        self.progress_bar.close()

        print("\nProcessing Completed")