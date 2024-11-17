import asyncio
import random
from typing import Any, Callable, Coroutine, TypedDict, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def check_results(current_result: str, new_result: str) -> bool:
    return current_result == new_result


# def compare_sync(
#     current_fn: Callable[[], T],
#     new_fn: Callable[[], T],
#     percentage: int,
#     logger_callback: Callable[[str], Coroutine[Any, Any, None]],
#     # html_file_name="example_profile.html"
# ):
#     pass


async def compare_async[T](
    current_fn: Callable[[], Coroutine[Any, Any, T]],
    new_fn: Callable[[], Coroutine[Any, Any, T]],
    percentage: int,
    logger_callback: Callable[[str], Coroutine[Any, Any, None]],
) -> T:
    # one file for each endpoint

    # make current production request
    current_result = await current_fn()

    # check if should make second request to compare
    total_request: int = 40
    compared_requests: int = 3
    percentage_of_total: int = round((compared_requests / total_request) * 100)
    should_compare = percentage_of_total < percentage and random.random() < 0.5

    # handle new result if needed
    new_result = ""
    if should_compare:
        new_result = await new_fn()

        has_equal_result = check_results(
            current_result=str(current_result), new_result=str(new_result)
        )

        log = {
            "is_equal": has_equal_result,
            "diff_trace": "",
        }

        await logger_callback(str(log))

    return current_result


# ANCHOR:


class Response(TypedDict):
    param1: int
    param2: str


async def useCase1(param1: int, param2: str) -> Response:
    return {"param1": param1, "param2": param2}


async def useCase2(param1: int, param2: str) -> Response:
    return {"param1": param1, "param2": param2}


async def logger(log: str) -> None:
    print(log)


async def controller() -> Response:
    current_fn = lambda: useCase1(param1=10, param2="nf24f8fn")
    new_fn = lambda: useCase2(param1=10, param2="nf24f8fnn")

    result = await compare_async(
        current_fn=current_fn,
        new_fn=new_fn,
        percentage=10,
        logger_callback=logger,
    )

    return result


if __name__ == "__main__":
    result = asyncio.run(controller())
    # print(result)
