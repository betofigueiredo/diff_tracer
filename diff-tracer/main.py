import os
import random
from typing import Any, Callable, Coroutine, TypeVar

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .diff_match_patch import diff_match_patch
from .utils import utils

T = TypeVar("T", bound=BaseModel)


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

                # save file with differences
                html_content = diff_match_patch().diff_prettyHtml(diffs=diff_content)
                utils.create_diff_result_file(html_content)

        # update main file on memory
        utils.update_main_file(total_requests, compared_requests, different_results)

        return current_result

    except Exception:
        return current_result


def init_web_view(app: FastAPI, security_token: str) -> None:
    def create_endpoint():
        async def endpoint(request: Request, token: str, filename: str):
            if token != security_token:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Not found"}
                )

            # get requests numbers
            total_requests = utils.get_main_file_value(key="total_requests", line=1)
            compared_requests = utils.get_main_file_value(
                key="compared_requests", line=2
            )
            different_results = utils.get_main_file_value(
                key="different_results", line=3
            )

            # get result files
            current_path = os.getcwd()
            target_folder = os.path.join(current_path, "tmp")
            result_files = []
            for file_name in os.listdir(target_folder):
                if file_name.startswith("result-") and file_name.endswith(".html"):
                    result_files.append(file_name)

            # get selected file content
            file_content: str = ""
            if filename:
                file_content = utils.get_result_file_content(filename)

            # return HTML
            templates = Jinja2Templates("diff-tracer")
            return templates.TemplateResponse(
                "view.html",
                {
                    "request": request,
                    "token": token,
                    "total_requests": total_requests,
                    "compared_requests": compared_requests,
                    "different_results": different_results,
                    "result_files": result_files,
                    "filename": filename,
                    "file_content": file_content,
                },
            )

        return endpoint

    app.add_api_route(
        "/diff-tracer-view/{token}",
        create_endpoint(),
        methods=["GET"],
        response_class=HTMLResponse,
    )
