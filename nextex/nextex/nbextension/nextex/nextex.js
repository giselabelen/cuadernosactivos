define([
    'base/js/namespace',
    'base/js/utils',
    './oauth-1.0a',
    './hmac-sha1',
    './enc-base64-min'
], function(
    Jupyter, utils, oauth, hmac, b64
) {
    function nextex_extension() {

        var handler = function () {

            var ajax = utils.ajax || $.ajax;

            var base_url = utils.get_body_data("baseUrl");
            var url = utils.url_path_join(base_url,'nextex');

            var settings = {
                dataType: 'json',
                success: function(json){    
                            // json -> deberia traer user y siguiente ejercicio (o algo que permita pedir el siguiente a PB)
                            lti_launch(json);
                            Jupyter.notebook.scroll_to_bottom();
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
        var oauth = OAuth({
            consumer: {
                key: 'otrakey',
                secret: 'estesecret'
            },
            // consumer: {
            //     key: '12345',
            //     secret: 'secret'
            // },
            signature_method: 'HMAC-SHA1',
            hash_function: function(base_string, key) {
                return CryptoJS.HmacSHA1(base_string, key).toString(CryptoJS.enc.Base64);
            }
        });

        var request_data = {
            //url: 'http://pilasbloques-staging.sadosky.net:5001/lti/',
            url: 'http://0.0.0.0:5000/lti/',
            //url: 'https://online.dr-chuck.com/sakai-api-test/tool.php',
            //url: 'http://api.pilasbloques-staging.sadosky.net:8000/lti/',
            method: 'POST',
            data: {
                lti_version : 'LTI-1p0',
                lti_message_type: 'basic-lti-launch-request',
                lis_outcome_service_url: 'http://localhost:82/outcomes/',
                lis_result_sourcedid: 'lala'
                //resource_link_id : 429785226,
                //user_id : 'pepe'
            }
        };

        var url = request_data.url;
        var type = request_data.method;
        var data = oauth.authorize(request_data);
        console.log(data);

        submitFORM(url,data,type);
    };

    function submitFORM(path, params, method) {
        var index = Jupyter.notebook.ncells();
        Jupyter.notebook.insert_cell_at_bottom('code');
        var new_cell = Jupyter.notebook.get_cell(index);

        method = method || "post"; 

        var div_launch = document.createElement("div");

        // creo el form
        var form = document.createElement("form");
        form.setAttribute("method", method);
        form.setAttribute("action", path);
        form.setAttribute("target", "basicLtiLaunchFrame");
        form.id = "basicLtiLaunchFrame";
        div_launch.appendChild(form);
        
        // creo el iframe
        var iframe = document.createElement("iframe");
        iframe.setAttribute("width", 750);
        iframe.setAttribute("height", 500);
        iframe.name = "basicLtiLaunchFrame";
        iframe.id = "basicLtiLaunchFrame";
        div_launch.appendChild(iframe);


        for(var key in params) {
            if(params.hasOwnProperty(key)) {
                var hiddenField = document.createElement("input");
                hiddenField.setAttribute("type", "hidden");
                hiddenField.setAttribute("name", key);
                hiddenField.setAttribute("value", params[key]);

                form.appendChild(hiddenField);
             }
        }

        // script que hace el submit
        var script = document.createElement("script");
        script.appendChild(document.createTextNode("document.getElementById(\"basicLtiLaunchFrame\").submit()"));
        div_launch.appendChild(script);

        // meto el launch en una celda, ejecuto y oculto el input para que solo se vea el iframe
        // requiere tener el nbextension hide_input para que se persista
        new_cell.set_text("%%html \n" + div_launch.innerHTML);
        new_cell.execute();
        new_cell.element.find("div.input").toggle();
        new_cell.metadata.hide_input = ! new_cell.metadata.hide_input;
    };

    return {
        load_ipython_extension: nextex_extension
    };
    
});
