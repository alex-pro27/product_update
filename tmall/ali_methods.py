# coding: utf8
from __future__ import absolute_import, unicode_literals

import json
from tmall.ali_request import AliexpressRequest
from config import AUTH_PARAMETERS


def _call_method(method, query, brand):
    request = AliexpressRequest.auth(**AUTH_PARAMETERS[brand])
    return request(dict(
        method=method,
        **query
    ))


def get_products(brand, current_page=1):
    """
    Получить все товары
    :param unicode brand: бренд
    :return: - вернет словарь {request_id: str, result: dict}
    :rtype dict
    """
    return _call_method(
        "aliexpress.solution.product.list.get",
        dict(
            aeop_a_e_product_list_query=json.dumps({
                'product_status_type':'onSelling',
                'current_page': current_page
            })
        ),
        brand
    )


def get_product_by_id(product_id, brand):
    """
    Получить полную инфу по товару
    :param int product_id: - ID товара их Али
    :param unicode brand: бренд
    """
    return _call_method(
        "aliexpress.postproduct.redefining.findaeproductbyid",
        dict(product_id=product_id),
        brand
    )


def update_sku_stocks(product_id, sku_stocks, brand):
    """
    Обновить остатки у товара
    :param int product_id: - ID товара их Али
    :param dict sku_stocks: - словарь где ключ это артикул товара, а значение - остатки
    :param unicode brand: бренд
    """
    return _call_method(
        "aliexpress.postproduct.redefining.findaeproductbyid",
        dict(
            product_id=product_id,
            sku_stocks=json.dumps(sku_stocks)
        ),
        brand
    )


def update_sku_price(product_id, sku_id, price, brand):
    """
    Обновить цену товара
    :param int product_id: - ID товара их Али
    :param unicode sku_id: - external id
    :param float price: Новая цена
    :param unicode brand: бренд
    """
    return _call_method(
        "aliexpress.postproduct.redefining.editsingleskuprice",
        dict(
            product_id=product_id,
            sku_id=sku_id,
            sku_price=price
        ),
        brand
    )
