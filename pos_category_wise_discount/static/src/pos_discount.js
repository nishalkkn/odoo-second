/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    async pay() {
        console.log('Discount limit :', this.pos.config.pos_discount_limit_bool);
//        console.log('Discount limit value :', this.pos.config.pos_disc_limit);
//        console.log('config :', this.pos.config);
    },
});
