from dataclasses import asdict
from typing import List, Dict

from flask import Response, jsonify

from backend.common.contracts import BaseResponse, PayloadData


def create_200_response() -> Response:
    response = Response()
    response.status_code = 200
    return response


def create_api_response(response: BaseResponse) -> Response:
    if response.success:
        if response.data is not None:
            return create_api_data_response(response.data)
        else:
            return create_200_response()
    else:
        return create_api_error_response(response.errors)


def create_api_data_response(payload_data: PayloadData) -> Response:
    data: Dict[str:Dict] = {'data': asdict(payload_data)}
    response: Response = jsonify(data)
    response.status_code = 200
    return response


def create_api_error_response(error_list: List[str], error_code: int = 400) -> Response:
    errors: Dict[str: List[str]] = {'errors': error_list}
    response: Response = jsonify(errors)
    response.status_code = error_code
    return response
