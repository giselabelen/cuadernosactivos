define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function check2_extension() {

    	

        var handler = function () {

            // celda con el resultado del alumno
			var cell_res = Jupyter.notebook.get_selected_cell();
			var text_res = cell_res.get_text();
            var index = Jupyter.notebook.get_selected_index();

            // celda con el ejercicio
            var cell_src = Jupyter.notebook.get_prev_cell(cell_res);
            var text_src = cell_src.get_text();
            var intento = cell_src.metadata.intento;

            // celda con la devolución
            Jupyter.notebook.insert_cell_below('raw');
			Jupyter.notebook.select(index+1,true);
			var new_cell = Jupyter.notebook.get_selected_cell();
			
            // devolución
            var correct = eval(text_src);
            if (correct == text_res) {
                new_cell.set_text("Terminaste a los " + intento + "intentos");
            } else {
                new_cell.set_text("2+1");
                new_cell.metadata.intento = intento+1;
            }



        };

        var action = {
            icon: 'fa-check-square-o', // a font-awesome class used on buttons, etc
            help    : 'chequear2',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'my_extension';
        var action_name = 'check2';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:check2'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    }

    return {
        load_ipython_extension: check2_extension
    };
});

