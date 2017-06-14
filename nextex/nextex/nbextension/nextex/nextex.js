define([
    'base/js/namespace',
    'base/js/utils',
    './oauth-1.0a',
    './hmac-sha1'
], function(
    Jupyter, utils, oauth, hmac
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
                            var new_cell = Jupyter.notebook.get_cell(index);
                            console.log(json);
                            //new_cell.set_text(JSON.stringify(json));
                            var url_lti_launch = lti_launch(json);
                            
                            new_cell.set_text(url_lti_launch);
                            
                            //new_cell.set_text("%%html \n <iframe width="750" height="500" src=" + url_lti_launch + "></iframe>");
                            new_cell.execute();
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


    function lti_launch(json){
        //var OAuth = require('./oauth-1.0a')

        var oauth = OAuth({
            consumer: {
                key: 'none',
                secret: 'none'
            },
            signature_method: 'HMAC-SHA1',
            hash_function: function(base_string, key) {
                return CryptoJS.HmacSHA1(base_string, key).toString(CryptoJS.enc.Base64);
            }
        });

        var request_data = {
            url: 'https://www.edu-apps.org/tool_redirect?id=educreations', // ver bien como testear esto
            method: 'POST',
            data: {
                lti_version : 'LTI-1p0',
                lti_message_type: 'basic-lti-launch-request',
                resource_link_id : 429785226
            }
        };

        // $.ajax({
        //     url: request_data.url,
        //     type: request_data.method,
        //     data: oauth.authorize(request_data)
        // }).done(function(data) {
        //     console.log(data)
        // });

        var url = request_data.url;
        var type = request_data.method;
        var data = oauth.authorize(request_data);

        return submitFORM(url,data,type);
    //     console.log("entre a la funcion");
    //     return JSON.stringify(json);
    };

    function submitFORM(path, params, method) {
        method = method || "post"; 

        var form = document.createElement("form");
        form.setAttribute("method", method);
        form.setAttribute("action", path);

        //Move the submit function to another variable
        //so that it doesn't get overwritten.
        form._submit_function_ = form.submit;

        for(var key in params) {
            if(params.hasOwnProperty(key)) {
                var hiddenField = document.createElement("input");
                hiddenField.setAttribute("type", "hidden");
                hiddenField.setAttribute("name", key);
                hiddenField.setAttribute("value", params[key]);

                form.appendChild(hiddenField);
             }
        }

        document.body.appendChild(form);

        var respuesta;

        form._submit_function_(function(data){
            respuesta = data;
        });

        return respuesta;
    };

    return {
        load_ipython_extension: nextex_extension
    };
    
});
