# coding: utf8
from __future__ import absolute_import, unicode_literals

import logging
from helpers import parse_xml_products
from pathos.multiprocessing import ThreadingPool
from tmall.models import Product, Brand
from tmall.ali_methods import update_sku_price, update_sku_stocks

logger = logging.getLogger("daemon_log")


class TmallService(object):

    def handle(self, message):
        # TODO Сделать роутинг по методам(Сейчас в xml не приходит название метода)
        self.update_products(message)

    def update_products(self, message):
        def update_product_callback(update_data):
            product = Product.objects(external_id=update_data["external_id"]).first()
            if not product:
                logger.warn("Product %s not found in database" % update_data["external_id"])
                return
            brand = Brand.objects(id=product.brand_id).first()

            ans = update_sku_price(
                product.product_id,
                product.external_id,
                update_data["price"],
                brand.name
            )

            if ans.get("error"):
                logger.error(
                    "Unable to update product(%s) price, message error: %s" % (
                        product.external_id,
                        ans.get("error_message")
                    )
                )
            else:
                logger.info(
                    "Product(%s) price, updated" % (
                        product.external_id,
                    )
                )
            ans = update_sku_stocks(
                product.product_id,
                update_data["stocks"],
                brand.name
            )
            if ans.get("error"):
                logger.error(
                    "Unable to update product(%s) stocks, message error: %s" % (
                        product.external_id,
                        ans.get("error_message")
                    )
                )
            else:
                logger.info(
                    "Product(%s) stocks, updated!" % (
                        product.external_id,
                    )
                )

        with ThreadingPool(nodes=4) as pool:
            pool.map(update_product_callback, parse_xml_products(message))