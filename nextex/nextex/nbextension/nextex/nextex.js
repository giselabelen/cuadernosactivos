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
            var url = utils.url_path_join(base_url,'corrector');

            // Nombre del alumno ---- hardcodeado por ahora
            var nombre = "pepe";

            // Número de ejercicio ---- hardcodeado por ahora
            var ejercicio = "1";

            // Texto introducido por el alumno
            var cell = Jupyter.notebook.get_selected_cell();
            var text = cell.get_text();

            var settings = {
                data : {
                    "nombre" : nombre,
                    "ejercicio" : ejercicio,
                    "respuesta" : text
                },
                type : 'POST',
                dataType: 'json',
                success: function(json){
                            console.log(json);
                            var index = Jupyter.notebook.get_selected_index();
                            Jupyter.notebook.insert_cell_below('raw');
                            Jupyter.notebook.select(index+1,true);
                            var new_cell = Jupyter.notebook.get_selected_cell();
                            if (json["aprobo"]) {
                                new_cell.set_text("Respondiste bien");
                            } else {
                                new_cell.set_text("Respondiste mal");
                            }
                        }
                };
            
            ajax(url, settings);
        };

/***************************************************************************************************************/

        var action = {
            icon: 'fa-plus-circle', // a font-awesome class used on buttons, etc
            help    : 'Siguiente Ejercicio',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'my_extension';
        var action_name = 'nextex';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:check'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    }

    return {
        load_ipython_extension: check_extension
    };
});
