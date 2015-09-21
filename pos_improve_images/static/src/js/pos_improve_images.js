/******************************************************************************
    Point Of Sale - Improve Images module for Odoo
    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
    @author Julien WESTE
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

openerp.pos_improve_images = function(instance){
    var module = instance.point_of_sale;

    /* ************************************************************************
    Overload :  Model 'ProductListWidget'
    - Overload get_product_image_url, depending on has_image value;
    ************************************************************************ */
    module.ProductListWidget = module.ProductListWidget.extend({

        get_product_image_url: function(product){
            if (product.has_image){
                return this._super(product);
            }
            else {
                return false;
            }
        },
        
        render_product: function(product){
            res = this._super(product);
            if (! product.has_image){
                // Hide image
                res.children[0].className = 'product-img product-img-without-image';
                // Change class of text
                res.children[1].className = 'product-name product-name-without-image';
            }
            return res;
        },
    });

    module.ProductCategoriesWidget = module.ProductCategoriesWidget.extend({
        render_category: function(category, with_image){
            res = this._super(category, with_image);
            if (with_image){
                if (! category.image){
                // Hide image
                res.children[0].className = 'category-img category-img-without-image';
                // Change class of text
                res.children[1].className = 'category-name category-name-without-image';
                }
            }
            return res;
        },
    });


    /* ************************************************************************
    Overload: point_of_sale.PosModel
    - Overload module.PosModel.initialize function to load extra-data
         - Load 'has_image' field from model product.template;
    ************************************************************************ */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        // Add the load of the field product_template.has_image
        for (var i = 0 ; i < this.models.length; i++){
            if (this.models[i].model == 'product.product'){
                if (this.models[i].fields.indexOf('has_image') == -1) {
                    this.models[i].fields.push('has_image');
                }
            }
            if (this.models[i].model == 'pos.category'){
                if (this.models[i].fields.indexOf('has_image') == -1) {
                    this.models[i].fields.push('has_image');
                }
            }
        }

        return _initialize_.call(this, session, attributes);
    };

};
