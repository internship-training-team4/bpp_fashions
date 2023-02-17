from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flaskapp.cache import cache
from flaskapp.api.products.services.product import ProductService
from flaskapp.api.products.services.search import SearchService
from flaskapp.schemas import PlainProductSchema, SearchSchema, ProductListSchema, PaginationSchema

blp = Blueprint("product", __name__, description="Operations on products")


@blp.route("/api/products/<string:product_id>")
class Product(MethodView):
    """Controller class for handling requests on products."""
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        product = ProductService.find_by_id(product_id)

        if product is None:
            search_params = {
                "q": product_id
            }

            search_data = SearchService.fire_search_query(search_params)
            status, response = SearchService.parse_search_results(search_data)

            if status != 200:
                abort(status, message=response)

            if response["total"] < 1:
                abort(404, message="Resource not found")

            return response["products"][0]

        return product


@blp.route("/api/products")
class ProductList(MethodView):
    """Controller class for handling requests on list of products."""
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(query_string=True)
    def get(self, pagination_params):
        products, total = ProductService.find_all(pagination_params)
        if len(products) == 0:
            abort(400, message="No match found")

        response = {
            "total": total,
            "rows": pagination_params.get("rows", current_app.config['PRODUCTS_PER_PAGE']),
            "products": products
        }

        return response


@blp.route("/api/search")
class ProductSearch(MethodView):
    """Controller class for handling search requests on products."""
    @blp.arguments(SearchSchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(query_string=True)
    def get(self, search_params):
        if "rows" not in search_params:
            search_params["rows"] = current_app.config["PRODUCTS_PER_PAGE"]

        search_data = SearchService.fire_search_query(search_params)
        status, response = SearchService.parse_search_results(search_data)

        if status != 200:
            abort(status, message=response)

        response["rows"] = search_params["rows"]

        return response


@blp.route("/api/products/categories/<int:category_id>")
class ProductCategory(MethodView):
    """Controller class for handling requests on products based on category type."""
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(query_string=True)
    def get(self, pagination_params, category_id):
        products, total = ProductService.find_by_category(category_id, pagination_params)

        if len(products) == 0:
            abort(400, message="No match found")

        response = {
            "total": total,
            "rows": pagination_params.get("rows", current_app.config['PRODUCTS_PER_PAGE']),
            "products": products
        }

        return response
