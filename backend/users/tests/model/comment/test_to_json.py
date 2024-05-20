


def test_comment_model_to_json(comment_model: User) -> None:
    result = comment_model.to_dict()
    assert comment_model.__dict__.items() > result.items()
