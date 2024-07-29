from typing import Optional, Dict
import json

import requests
from flask_restful import abort

from api.const import SUCCESS_STATUS_CODES


def make_request(
    *,
    url: str,
    headers: Dict,
    method: str = 'GET',
    body: Optional[Dict] = None,
    params: Optional[Dict] = None,
    files: Optional[Dict] = None,
    timeout: int = 30,
):
    """_summary_

    Args:
        url (str): _description_
        headers (Dict): _description_
        method (str, optional): _description_. Defaults to 'GET'.
        body (Optional[Dict], optional): _description_. Defaults to None.
        params (Optional[Dict], optional): _description_. Defaults to None.
        files (Optional[Dict], optional): _description_. Defaults to None.
        timeout (int, optional): _description_. Defaults to 30.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    response = requests.request(
        method=method,
        url=url,
        params=params,
        data=json.dumps(body),
        headers=headers,
        files=files,
        timeout=timeout,
    )

    if response.status_code not in SUCCESS_STATUS_CODES:
        abort(response.status_code, message=response.text)

    return response
