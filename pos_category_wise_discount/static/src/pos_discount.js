/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
patch(Order.prototype, {
    async pay() {
        if (this.pos.config.is_pos_discount_limit) {
            var dictionary = {}
            var discount_limit = this.pos.config.pos_discount_limit
            for (var i = 0; i < this.orderlines.length; i++) {
                var product_categ_id = this.orderlines[i].product.pos_categ_ids
                var discount = this.orderlines[i].price * (this.orderlines[i].discount / 100)
                if (product_categ_id in dictionary) {
                    dictionary[product_categ_id] += discount
                } else {
                    dictionary[product_categ_id] = discount
                }
            }
            var keys = Object.keys(dictionary)
            for (var i = 0; i < keys.length; i++) {
                if ((dictionary[keys[i]]) > discount_limit) {
                    var limit = 1
                }
            }
            if (limit == 1) {
                 this.env.services.popup.add(ErrorPopup, {
                    title: "Discount limit",
                    body: "Category wise discount limit reached !!!",
                });
            } else {
                return {
                    ...super.pay(...arguments)
                }
            }
        }
        return {
            ...super.pay(...arguments)
        }
    },
});
