from typing import Any, Generator

import pytest

from diff_tracer.main import compare_async
from diff_tracer.utils import utils


# basic test request
async def current_fn() -> dict[str, Any]:
    return {"users": [{"name": "John"}]}


# basic test request
async def new_equal_fn() -> dict[str, Any]:
    return {"users": [{"name": "John"}]}


# basic test request
async def new_diff_fn() -> dict[str, Any]:
    return {"users": [{"name": "Doe"}]}


@pytest.fixture(autouse=True)
def run_before_and_after_tests() -> Generator[Any, Any, Any]:
    """Fixture to execute asserts before and after a test is run"""
    yield
    # clear folder data after each test
    utils.clear_saved_data()


@pytest.mark.asyncio
class TestCompareAsync:
    # TEST:
    async def test_main_return(self) -> None:
        """should always return the result of the current production function"""

        response = await compare_async(
            current_fn=lambda: current_fn(),
            new_fn=lambda: new_diff_fn(),
            percentage=80,
        )
        assert response == await current_fn()
        assert response.get("users", [])[0].get("name") == "John"

    # TEST:
    async def test_total_requests_count(self) -> None:
        """should count all requests and save in local file"""

        for _ in range(2):
            await compare_async(
                current_fn=lambda: current_fn(),
                new_fn=lambda: new_equal_fn(),
                percentage=100,
            )
        total_requests = utils.get_main_file_value(key="total_requests", line=1)
        assert total_requests == 2

    # TEST:
    async def test_compared_requests(self) -> None:
        """should count compared requests and save in local file"""

        for _ in range(10):
            await compare_async(
                current_fn=lambda: current_fn(),
                new_fn=lambda: new_diff_fn(),
                percentage=100,
            )
        compared_requests = utils.get_main_file_value(key="compared_requests", line=2)
        assert compared_requests > 0

    # TEST:
    async def test_diff_requests(self) -> None:
        """should count different requests and save in local file"""

        for _ in range(6):
            await compare_async(
                current_fn=lambda: current_fn(),
                new_fn=lambda: new_diff_fn(),
                percentage=100,
            )
        different_results = utils.get_main_file_value(key="different_results", line=3)
        assert different_results > 0
        result_files = utils.get_all_results_files()
        assert len(result_files) > 0

    # TEST:
    @pytest.mark.skip(reason="TODO: Not implemented yet")
    async def test_only_work_with_dicts(self) -> None:
        """should only work with dicts"""
        pass
