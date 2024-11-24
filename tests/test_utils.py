import os
from unittest.mock import patch

from diff_tracer.utils import utils


class TestUtils:
    # TEST:
    def test_get_target_path(self) -> None:
        target_path = utils.get_target_path()
        expected_path = os.path.join(os.getcwd(), "tmp-diff-tracer")
        assert target_path == expected_path

    # TEST:
    def test_get_main_file_path(self) -> None:
        main_file_path = utils.get_main_file_path()
        expected_path = os.path.join(
            os.getcwd(), "tmp-diff-tracer", "diff-tracer-main-info.txt"
        )
        assert main_file_path == expected_path

    # TEST:
    def test_get_main_file_value(self) -> None:
        with patch("linecache.getline") as mock_getline:
            mock_getline.return_value = "total_requests=5"
            result = utils.get_main_file_value("total_requests", 1)
            assert result == 5
