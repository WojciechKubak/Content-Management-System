from users.model.comment import CommentModel
from users.extensions import sa
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(scope='function', autouse=True)
def add_comment(app: Flask, comment_model_data: dict[str, Any]) -> None:
    sa.session.add(CommentModel(**comment_model_data))
    sa.session.commit()
