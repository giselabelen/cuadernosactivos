define([
    'base/js/namespace',
    'base/js/utils'
], function(
    Jupyter, utils
) {
    function seguimiento_extension() {

        var handler = function () {

            var ajax = utils.ajax || $.ajax;

            var base_url = utils.get_body_data("baseUrl");
            var url = utils.url_path_join(base_url,'seguimiento');

            // leo de la metadata de la celda seleccionada y la solucion de le alumne
            var cell = Jupyter.notebook.get_selected_cell();
            var id_guia = cell.metadata.id_guia;
            var id_ejercicio = cell.metadata.id_ejercicio;
            var resolucion = cell.get_text();
            // envio sol actual y recibo ejercicio sig
            var settings = {
                data : {
                    "id_guia" : id_guia,
                    "id_ejercicio" : id_ejercicio,
                    "resolucion" : resolucion,
                    "timestamp" : Date.now()
                },
                type : 'POST',
                dataType: 'json',
                success: function(json){
                            
                            var ejercicio = json["ejercicio"];
                            id_guia = json["id_guia"];
                            id_ejercicio = json["id_ejercicio"];
                            var texto = "";

                            var index = Jupyter.notebook.get_selected_index();
                            
                            Jupyter.notebook.insert_cell_below('markdown');
                            Jupyter.notebook.select(index+1,true);
                            var celda_ej = Jupyter.notebook.get_selected_cell();
                            
                            if (id_guia == 0) {
                                texto = "## "+ejercicio;
                            }else{
                                if (id_ejercicio == 1) {
                                    texto = "# Guia "+id_guia+"\n";
                                }
                                texto += "### Ejercicio "+id_ejercicio+"\n Resolver: "+ejercicio;
                            }
                            
                            celda_ej.set_text(texto);
                            Jupyter.notebook.execute_selected_cells()
                            
                            Jupyter.notebook.insert_cell_below('raw');
                            Jupyter.notebook.select(index+2,true);
                            var celda_sol = Jupyter.notebook.get_selected_cell();
                            celda_sol.metadata = {
                                                    'id_guia':id_guia,
                                                    'id_ejercicio':id_ejercicio
                                                }
                            celda_sol.focus_editor()
                        }
                };
            
            ajax(url, settings);

        };

/***************************************************************************************************************/

        var action = {
            icon: 'fas fa-certificate', // a font-awesome class used on buttons, etc
            help    : 'caso con seguimiento',
            //help_index : 'zz',
            handler : handler
        };
        var prefix = 'my_extension';
        var action_name = 'seguimiento';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:seguimiento'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    }

    return {
        load_ipython_extension: seguimiento_extension
    };
});
