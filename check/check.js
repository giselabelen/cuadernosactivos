define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function check_extension() {

    	

        var handler = function () {
            //alert('this is an alert from my new extension!');
/*
            Jupyter.notebook.copy_cell();
			Jupyter.notebook.paste_cell_below();
*/	

/*
			Jupyter.notebook.scroll_to_bottom();
			var n = Jupyter.notebook.ncells();
			Jupyter.notebook.insert_cell_at_index('markdown',n-1);
			
			Jupyter.notebook.select(n-1,true);
			var cell = Jupyter.notebook.get_selected_cell();
			cell.set_text("nuevo contenido");
			//console.log(Jupyter.notebook.get_selected_cell().code_mirror.display.lineDiv.textContent);
			Jupyter.notebook.execute_cell();*/


            // Texto introducido por el alumno
			var cell = Jupyter.notebook.get_selected_cell();
			var text = cell.get_text();
			console.log(text);

            /*  armar el json con el nombre, el ejercicio y el texto introducido por el alumno
            *   hacer el POST a /localhost:80/corrector usando $post() --ver ajax--
            *   recibir la respuesta del servidor
            *   procesar la respuesta del servidor
            *   generar una nueva celda mostrando la corrección del servidor --aprovechar params de $post()-- */


			var index = Jupyter.notebook.get_selected_index();
			Jupyter.notebook.insert_cell_below('code');
			Jupyter.notebook.select(index+1,true);
			var new_cell = Jupyter.notebook.get_selected_cell();
			new_cell.set_text("%%bash \n for i in {1..5}; do echo " + text + "; done");
			Jupyter.notebook.execute_cell();


        };

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
