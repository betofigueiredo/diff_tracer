import asyncio
import random
from typing import Any, Callable, Coroutine, TypedDict, TypeVar

from diff_match_patch import diff_match_patch
from pydantic import BaseModel
from utils import utils

T = TypeVar("T", bound=BaseModel)


# def compare_sync(
#     current_fn: Callable[[], T],
#     new_fn: Callable[[], T],
#     percentage: int,
#     logger_callback: Callable[[str], Coroutine[Any, Any, None]],
#     # html_file_name="example_profile.html"
# ):
#     pass

MAIN_FILE_NAME = "diff-tracer-main-info.txt"


async def compare_async[T](
    current_fn: Callable[[], Coroutine[Any, Any, T]],
    new_fn: Callable[[], Coroutine[Any, Any, T]],
    percentage: int,
) -> T:
    # make current production request
    current_result = await current_fn()

    try:
        # get previous data
        total_requests = utils.get_main_file_value(key="total_requests", line=1)
        compared_requests = utils.get_main_file_value(key="compared_requests", line=2)
        different_results = utils.get_main_file_value(key="different_results", line=3)

        # count current request
        total_requests += 1

        # check if should make second request to compare
        percentage_of_total: int = round((compared_requests / total_requests) * 100)
        should_compare = percentage_of_total < percentage and random.random() < 0.5

        # handle new result if needed
        if should_compare:
            compared_requests += 1
            new_result = await new_fn()
            is_equal, diff_content = diff_match_patch().diff_main(
                text1=str(current_result), text2=str(new_result)
            )
            if not is_equal:
                different_results += 1
                html_content = diff_match_patch().diff_prettyHtml(diffs=diff_content)
                utils.create_diff_result_file(html_content)

        utils.update_main_file(total_requests, compared_requests, different_results)

        return current_result

    except Exception:
        return current_result


# ANCHOR:


class Response(TypedDict):
    param1: int
    param2: str


async def useCase1(param1: int, param2: str) -> Response:
    return {"param1": param1, "param2": param2}


async def useCase2(param1: int, param2: str) -> Response:
    return {"param1": param1, "param2": param2}


async def controller() -> Response:
    current_fn = lambda: useCase1(param1=10, param2="nf24f8fn")
    new_fn = lambda: useCase2(param1=11, param2="nf24f8fn")

    result = await compare_async(
        current_fn=current_fn,
        new_fn=new_fn,
        percentage=80,
    )

    return result


if __name__ == "__main__":
    result = asyncio.run(controller())
    # print(result)
