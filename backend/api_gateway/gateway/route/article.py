from gateway.security.role_auth import requires_roles
from gateway.service.configuration import article_service
from gateway.extensions import cache
from flask import Blueprint, Response, make_response, request
from typing import Any

article_blueprint = Blueprint('articles', __name__, url_prefix='/api/articles')


def handle_article_request(method: str, endpoint: str, data: dict[str, Any] | None = None) -> Response:
    try:
        response_data, status_code = article_service.process_request(method, endpoint, data)
        return make_response(response_data, status_code)
    except ConnectionError as e:
        return make_response({'message': str(e)}, 500)


@article_blueprint.route('/health', methods=['GET'])
@requires_roles(['admin'])
def health_check() -> Response:
    try:
        article_service.check_health()
        return make_response({'message': 'Articles service is working'}, 200)
    except ConnectionError as e:
         return make_response({'message': str(e)}, 500)


@article_blueprint.route('/<int:article_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_article(article_id: int) -> Response:
    return handle_article_request(request.method, f'articles/{article_id}')


@article_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=50)
def get_articles() -> Response:
    return handle_article_request(request.method, f'articles/')


@article_blueprint.route('/category/<int:category_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_category_articles(category_id: int) -> Response:
    return handle_article_request(request.method, f'articles/category/{category_id}')


@article_blueprint.route('/', methods=['POST'])
@requires_roles(['admin', 'redactor'])
def post_article() -> Response:
    return handle_article_request(request.method, 'articles', request.json)


@article_blueprint.route('/<int:article_id>', methods=['PUT'])
@requires_roles(['admin', 'redactor'])
def put_article(article_id: int) -> Response:
    return handle_article_request(request.method, f'articles/{article_id}', request.json)


@article_blueprint.route('/<int:article_id>', methods=['DELETE'])
@requires_roles(['admin', 'redactor'])
def delete_article(article_id: int) -> Response:
    return handle_article_request(request.method, f'articles/{article_id}')


@article_blueprint.route('categories/<int:category_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_category(category_id: int) -> Response:
    return handle_article_request(request.method, f'articles/categories/{category_id}')


@article_blueprint.route('/categories', methods=['GET'])
@cache.cached(timeout=50)
def get_categories() -> Response:
    return handle_article_request(request.method, f'articles/categories/')


@article_blueprint.route('/categories', methods=['POST'])
@requires_roles(['admin', 'redactor'])
def post_category() -> Response:
    return handle_article_request(request.method, f'articles/categories', request.json)


@article_blueprint.route('/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@requires_roles(['admin', 'redactor'])
def put_category(category_id: int) -> Response:
    return handle_article_request(request.method, f'articles/categories/{category_id}', request.json)


@article_blueprint.route('/<int:article_id>', methods=['DELETE'])
@requires_roles(['admin', 'redactor'])
def delete_category(article_id: int) -> Response:
    return handle_article_request(request.method, f'articles/categories/{article_id}')


@article_blueprint.route('tags/<int:tag_id>', methods=['GET'])
@cache.cached(timeout=50)
def get_tag(tag_id: int) -> Response:
    return handle_article_request(request.method, f'articles/tags/{tag_id}')


@article_blueprint.route('/tags', methods=['GET'])
@cache.cached(timeout=50)
def get_tags() -> Response:
    return handle_article_request(request.method, f'articles/tags/')


@article_blueprint.route('/tags', methods=['POST'])
@requires_roles(['admin', 'redactor'])
def post_tag() -> Response:
    return handle_article_request(request.method, f'articles/tags', request.json)


@article_blueprint.route('/tags/<int:tag_id>', methods=['PUT'])
@requires_roles(['admin', 'redactor'])
def put_tag(tag_id: int) -> Response:
    return handle_article_request(request.method, f'articles/tags/{tag_id}', request.json)


@article_blueprint.route('tags/<int:tag_id>', methods=['DELETE'])
@requires_roles(['admin', 'redactor'])
def delete_tag(tag_id: int) -> Response:
    return handle_article_request(request.method, f'articles/tags/{tag_id}')
