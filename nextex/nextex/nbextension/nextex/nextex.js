define([
    'base/js/namespace',
    'base/js/utils',
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
                            
                            var index = Jupyter.notebook.ncells();
                            Jupyter.notebook.insert_cell_at_bottom('raw');
                            console.log(json);
                            var new_cell = Juptyter.notebook.get_cell(index);   // <-- ACA HAY PROBLEMAS --- REVISAR!!!!!
                            
                            // var url_lti_launch = lti_launch(json);
                            // console.log("estoy por setear el texto");
                            // new_cell.set_text(url_lti_launch);

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
    };

    //function lti_launch(json){

        // var oauth = OAuth({
        //     consumer: {
        //         key: 'notebook',
        //         secret: 'sarasa'
        //     },
        //     signature_method: 'HMAC-SHA1',
        //     hash_function: function(base_string, key) {
        //         return CryptoJS.HmacSHA1(base_string, key).toString(CryptoJS.enc.Base64);
        //     }
        // });

        // var request_data = {
        //     url: 'urlDePilasBloques',
        //     method: 'POST',
        //     data: {
        //         lti_version : 'LTI-1p0',
        //         lti_message_type: 'basic-lti-launch-request',
        //         resource_link_id : 1
        //     }
        // };

        // $.ajax({
        //     url: request_data.url,
        //     type: request_data.method,
        //     data: oauth.authorize(request_data, token)
        // }).done(function(data) {
        //     //process your data here
        // });
    //     console.log("entre a la funcion");
    //     return json;
    // };

    return {
        load_ipython_extension: nextex_extension
    };
    
});
