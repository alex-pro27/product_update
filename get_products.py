# coding: utf8
from __future__ import absolute_import, unicode_literals

import logging
from pathos.multiprocessing import ThreadingPool
from tmall.ali_methods import get_products, get_product_by_id
from tmall.models import Product, Brand
from config import AUTH_PARAMETERS

logger = logging.getLogger("tmall_log")


def create_product_callback(brand, product_info):
    """
    :param Brand brand:
    :param dict product_info:
    :return:
    """
    product = Product.objects(product_id=product_info["product_id"]).first()

    if product:
        return

    product = Product(
        name=product_info["subject"],
        product_id=product_info["product_id"],
        brand_id=brand.id,
    )
    ans = get_product_by_id(product.product_id, brand.name)
    if ans.get("error_code"):
        logger.error(
            "failed to load product - %s, brand %s, error message: %s" % (
                product.name,
                brand.name,
                ans.get("error_message")
            )
        )
        return
    try:
        external_id = ans["result"]["aeop_ae_product_s_k_us"]["aeop_ae_product_sku"][0]["sku_code"]
        product.external_id = external_id
        product.save()
        brand.products.append(product)
        # brand.products = list(set(brand.products))
        brand.save()
        logger.info("created product %s for brand: %s" % (product.name, brand.name))
    except (KeyError, IndexError) as e:
        logger.error(
            "failed get product: %s -  %s" % (
                e.message,
                ans,
            )
        )

def get_products_callback(brand, page=1):
    """
    :param Brand brand:
    :param int page:
    :return:
    """
    ans = get_products(brand.name, page)
    if ans.get("error_code"):
        logger.error(
            "failed to load brand - %s: page: %s, error message: %s" % (
                brand.name,
                page,
                ans.get("error_message")
            )
        )
        return
    print "getting products for brand: %s, page: %s ..." % (brand.name, page)
    res = ans["result"]
    products_list = res["aeop_a_e_product_display_d_t_o_list"]["item_display_dto"]

    with ThreadingPool(nodes=20) as pool:
        pool.map(lambda product_info: create_product_callback(brand, product_info), products_list)

    total_page = int(res["total_page"])
    if page != total_page:
        get_products_callback(brand, page + 1)


def get_all_brands_products():

    brands = []
    for brand_name in AUTH_PARAMETERS.keys():
        brand = Brand.objects(name=brand_name).first()
        if not brand:
            brand = Brand(name=brand_name)
            brand.save()
        brands.append(brand)

    with ThreadingPool(nodes=4) as pool:
        pool.map(get_products_callback, brands)


if __name__ == "__main__":
    get_all_brands_products()
