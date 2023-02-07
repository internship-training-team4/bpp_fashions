from flaskapp import db
from flaskapp.dal.product import ProductDAL


class ProductService:
    @classmethod
    def parse_sort_parameters(cls, parameters):
        if "sort" in parameters and parameters["sort"].lower().split()[0] == "price":
            sort_field = "price"
            sort_order = parameters["sort"].lower().split()[-1]
            reverse = False

            if sort_order == "desc":
                reverse = True

            return sort_field, reverse

        return None, None

    @classmethod
    def parse_pagination_parameters(cls, parameters):
        page = parameters.get("page", 1)
        rows = parameters.get("rows", None)
        return page, rows

    @classmethod
    def find_by_id(cls, id):
        return ProductDAL.find_by_id(db, id)

    @classmethod
    def find_all(cls, parameters):
        sort_field, reverse = cls.parse_sort_parameters(parameters)
        page, rows = cls.parse_pagination_parameters(parameters)

        products = ProductDAL.find_all(db, sort_field, reverse, page, rows)
        total = ProductDAL.count_all(db)

        return products, total

    @classmethod
    def find_by_category(cls, category_id, parameters):
        sort_field, reverse = cls.parse_sort_parameters(parameters)
        page, rows = cls.parse_pagination_parameters(parameters)

        products = ProductDAL.find_by_category_id(db, category_id, sort_field, reverse, page, rows)
        total = ProductDAL.count_by_category_id(db, category_id)

        return products, total