import linecache
import os
from datetime import datetime

MAIN_FILE_NAME = "diff-tracer-main-info.txt"


class Utils:
    def get_target_path(self) -> str:
        current_path = os.getcwd()
        return os.path.join(current_path, "tmp")

    def get_main_file_path(self) -> str:
        target_path = self.get_target_path()
        os.makedirs(target_path, exist_ok=True)
        return os.path.join(target_path, MAIN_FILE_NAME)

    def get_main_file_value(self, key: str, line: int) -> int:
        main_info_file_path = self.get_main_file_path()
        value = int(
            (linecache.getline(main_info_file_path, line) or f"{key}=0")
            .replace("\n", "")
            .replace("\r", "")
            .replace(f"{key}=", "")
        )
        linecache.clearcache()
        return value

    def update_main_file(
        self, total_requests: int, compared_requests: int, different_results: int
    ) -> None:
        main_info_file_path = self.get_main_file_path()
        with open(main_info_file_path, "w") as wb:
            lines = [
                f"total_requests={str(total_requests)}\n",
                f"compared_requests={str(compared_requests)}\n",
                f"different_results={str(different_results)}\n",
            ]
            wb.writelines(lines)

    def create_diff_result_file(self, html_content: str) -> None:
        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"result-{today}.html"
        target_path = self.get_target_path()
        file_location = os.path.join(target_path, file_name)
        with open(file_location, "w") as buffer:
            buffer.write(html_content)

    def get_result_file_content(self, filename: str) -> str:
        target_path = self.get_target_path()
        file_location = os.path.join(target_path, filename)
        file_exists = os.path.isfile(file_location)
        if file_exists:
            with open(file_location, "r") as buffer:
                return buffer.read()
        return ""


utils = Utils()
