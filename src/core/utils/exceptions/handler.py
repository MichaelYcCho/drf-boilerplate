from __future__ import annotations

import logging
from typing import Any, Optional

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

VALIDATION_ERROR_CODE = 999999


def core_exception_handler(exc: Any, context: Any) -> Optional[Response]:
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, context)
    if response is not None:
        try:
            exc.default_detail
        except Exception as e:
            logging.info(f"core_exception_handler {e}")

        error_detail = exc.args if isinstance(exc, Http404) else exc.default_detail
        data = {
            "error_code": getattr(exc, "error_code", "None"),
            "error_detail": error_detail,
        }

        if isinstance(exc, serializers.ValidationError):
            error_keys = list(response.data.keys())
            data["error_code"] = VALIDATION_ERROR_CODE
            data["error_detail"] = f"{error_detail} : {error_keys}"
            response.data = data
            logging.error(f"[Exception] - ValidationError {exc}")
        else:
            error_detail = response.data.pop("detail", None)
            targets = [
                (
                    {"string": str(error_detail), "code": error_detail.code}  # type: ignore
                    if error_detail is not None
                    else "N/A"
                )
            ]
            data["targets"] = targets
            response.data.update(data)
        if response.data["error_code"] != VALIDATION_ERROR_CODE:
            response.data.pop("targets", None)
    return response
