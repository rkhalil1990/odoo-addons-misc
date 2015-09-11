/******************************************************************************
    Point Of Sale - Street Market module for Odoo
    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

function load__pos_street_market__widget(instance) {

    module = instance.point_of_sale;

/* ****************************************************************************
Overload: point_of_sale.PosWidget

- Add a new PopUp select_market_place_popup in the PopUp List;
**************************************************************************** */

    module.PosWidget = module.PosWidget.extend({

        /* Overload Section */
        build_widgets: function(){
            this._super();

            var self = this;

            // Create new PopUp
            this.select_market_place_popup = new module.SelectMarketPlacePopupWidget(this, {});
            this.select_market_place_popup.appendTo($(this.$el));

            // Hide the popup because all new PopUp are displayed by default
            this.select_market_place_popup.hide();

            // Add the New PopUp to the screen selector
            this.screen_selector.popup_set['select-market-place-popup'] = this.select_market_place_popup;

            // Add On click behaviour to display the PopUp
            this.$('#button_select_market_place').click(function () {
                self.screen_selector.show_popup('select-market-place-popup');
            })
        },

    });

/* ****************************************************************************
Define : pos_street_market.SelectMarketPlacePopupWidget
    
- This widget display a pop up to select a Market Place that will be used for
  all the next PoS Orders;
- Add the possibility to unset a selecte Market Place;
**************************************************************************** */

    module.SelectMarketPlacePopupWidget = module.PopUpWidget.extend({
        template:'SelectMarketPlacePopupWidget',

//        /* Overload Section */
        start: function(){
            this._super();
            var self = this;
            // Add On click behaviour to hide the PopUp
            this.$('#market-place-empty').click(function () {
                self.pos_widget.screen_selector.close_popup();
            });
        },


    });

}
