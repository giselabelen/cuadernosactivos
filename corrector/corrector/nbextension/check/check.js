define([
    'base/js/namespace',
    'base/js/utils'
], function(
    Jupyter, utils
) {
    function check_extension() {

        var handler = function () {

/****************************************************************************************************************
 ****************************************************************************************************************

        PARTE DE LA POC EN LA QUE LA NBEXTENSION SE COMUNICA DIRECTO CON EL BACKEND QUE TOMA DECISIONES

****************************************************************************************************************
****************************************************************************************************************/

            /*  armar el json con el nombre, el ejercicio y el texto introducido por el alumno
            *   hacer el POST a /localhost:80/corrector usando $post() --ver ajax--
            *   recibir la respuesta del servidor
            *   procesar la respuesta del servidor
            *   generar una nueva celda mostrando la corrección del servidor --aprovechar params de $post()-- */


/*            // Nombre del alumno ---- hardcodeado por ahora
            var nombre = "pepe";

            // Número de ejercicio ---- hardcodeado por ahora
            var ejercicio = "1";

            // Texto introducido por el alumno
            var cell = Jupyter.notebook.get_selected_cell();
            var text = cell.get_text();
            //console.log(text);

            // Json con todo para el request
            var datos = {
                            "nombre" : nombre,
                            "ejercicio" : ejercicio,
                            "respuesta" : text
                        }

            // $.post("http://localhost:80/corrector/",
            //         datos,
            //         function(json){
            //             console.log(json);
            //         },
            //         "json");

            $.ajax({
                url: "http://localhost:80/corrector/",
                type: 'post',
                data: datos,
                //contentType: "application/json", // The 'contentType' property sets the 'Content-Type' header.
//                headers: { "Content-Type": "application/json" },
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
            });
*/

/****************************************************************************************************************
 ****************************************************************************************************************

 PARTE DE LA POC EN LA QUE LA NBEXTENSION SE COMUNICA CON EL BACKEND QUE TOMA DECISIONES A TRAVES DEL NBSERVER
        
****************************************************************************************************************
****************************************************************************************************************/

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

			// var index = Jupyter.notebook.get_selected_index();
			// Jupyter.notebook.insert_cell_below('code');
			// Jupyter.notebook.select(index+1,true);
			// var new_cell = Jupyter.notebook.get_selected_cell();
			// new_cell.set_text("%%bash \n for i in {1..5}; do echo " + text + "; done");
			// Jupyter.notebook.execute_cell();
        };

/***************************************************************************************************************/

        var action = {
            icon: 'fa-check-square', // a font-awesome class used on buttons, etc
            help    : 'chequear',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'my_extension';
        var action_name = 'check';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:check'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    }

    return {
        load_ipython_extension: check_extension
    };
});
