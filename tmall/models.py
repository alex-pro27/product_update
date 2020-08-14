# coding: utf8
import mongoengine


class Product(mongoengine.Document):

    name = mongoengine.StringField()
    product_id = mongoengine.IntField()
    article = mongoengine.StringField()
    external_id = mongoengine.StringField()
    brand_id = mongoengine.ObjectIdField()

    meta = {'strict': False, 'collection': 'products'}

    def __hash__(self):
        return hash(self.product_id)

    def __repr__(self):
        return self.name


class Brand(mongoengine.Document):

    name = mongoengine.StringField()
    products = mongoengine.ListField(mongoengine.ReferenceField(Product))

    meta = {'strict': False, 'collection': 'brands'}

    def __repr__(self):
        return self.name