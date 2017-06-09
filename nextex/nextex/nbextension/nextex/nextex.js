define([
    'base/js/namespace',
    'base/js/utils'
], function(
    Jupyter, utils
) {
    function nextex_extension() {

        var handler = function () {

            var ajax = utils.ajax || $.ajax;

            var base_url = utils.get_body_data("baseUrl");
            var url = utils.url_path_join(base_url,'nextex');

            var settings = {
                // data : {
                //     "nombre" : nombre,
                //     "ejercicio" : ejercicio,
                //     "respuesta" : text
                // },
                // type : 'POST',
                dataType: 'json',
                success: function(json){    // json -> deberia traer user y siguiente ejercicio (o algo que permita pedir el siguiente a PB)
                            /* CREAR NUEVA CELDA AL FINAL
                             * HACER LTI LAUNCH
                             * METER EN LA CELDA EL IFRAME CON EL URL DE PB
                             * EJECUTAR LA CELDA
                             */
                            console.log(json);
                            var index = Jupyter.notebook.ncells();
                            Jupyter.notebook.insert_cell_at_bottom('code');
                            var new_cell = Juptyter.notebook.get_cell(index);

                            //var url_lti_launch = lti_launch();

                            //new_cell.set_text("%%html \n <iframe width="750" height="500" src=" + url_lti_launch + "></iframe>");
                            //new_cell.execute();
                        }
                };
            
            ajax(url, settings);

         };

        var action = {
            icon: 'fa-plus-circle', // a font-awesome class used on buttons, etc
            help    : 'Siguiente Ejercicio',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'my_extension';
        var action_name = 'nextex';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:nextex'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    }

    return {
        load_ipython_extension: nextex_extension
    };
    
});
