/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { useRef, onWillRender, onMounted, Component } from "@odoo/owl";
import { parseFloat } from "@web/views/fields/parsers";

export class FloatInt extends Component {
    static template = "float_int_widget.MathField";
    setup() {
        this.input = useRef('inputmathfield'),
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            refName: "inputmathfield",
            parse: (v) => parseFloat(v),
        });
        onWillRender(() => {
            this.rounded()
        });
        onMounted(() => {
            this.rounded()
        });
    }
    rounded() {
        if (this.input.el) {
            this.props.record.data[this.props.name] = Math(this.input.el.value)
        }
    }
}
FloatInt.component = FloatInt
//FloatInt.supportedTypes = ["float"]
registry.category("fields").add("float_int_widget", FloatInt);