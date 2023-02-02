from flaskapp.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer


class CategoryModel(Base):
    __tablename__ = "category"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(50))
    level = Column(Integer)

    def __repr__(self):
        return f"Category('{self.id}', '{self.parent_id}', '{self.name}', '{self.level}')"

    @classmethod
    def find_by_id_query(cls, db, id):
        return db.query(cls).filter(cls.id == id)

    @classmethod
    def find_all_query(cls, db):
        return db.query(cls)

    @classmethod
    def find_by_level_query(cls, db, level):
        return db.query(cls).filter(cls.level == level)

    @classmethod
    def find_all_children_query(cls, db, category_id):
        return db.query(cls).filter(cls.parent_id == category_id)

    @classmethod
    def find_if_exists_query(cls, db, parent_id=None, name=None, level=None):
        q = db.query(cls)
        if parent_id is not None:
            q = q.filter(cls.parent_id == parent_id)
        if name is not None:
            q = q.filter(cls.name == name)
        if level is not None:
            q = q.filter(cls.level == level)
        return q

        return db.query(CategoryModel) \
            .filter(CategoryModel.parent_id == self.parent_id) \
            .filter(CategoryModel.name == self.name) \
            .filter(CategoryModel.level == self.level) \
            .first() is not None

    @classmethod
    def find_by_id(cls, db, id):
        return cls.find_by_id_query(db, id).first()

    @classmethod
    def find_all(cls, db):
        return cls.find_all_query(db).all()

    @classmethod
    def find_by_level(cls, db, level):
        return cls.find_by_level_query(db, level).all()

    @classmethod
    def find_all_parents(cls, db, category_id):
        return cls.find_all_children_query(db, category_id)

    @classmethod
    def find_if_exists(cls, db, parent_id=None, name=None, level=None):
        return cls.find_if_exists_query(db, parent_id, name, level).first()

        return db.query(CategoryModel)\
            .filter(CategoryModel.parent_id == self.parent_id)\
            .filter(CategoryModel.name == self.name)\
            .filter(CategoryModel.level == self.level)\
            .first() is not None

    def save(self, db):
        db.add(self)
