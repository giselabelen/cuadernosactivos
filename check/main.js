define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function check_extension() {

		var handler = function() {
		    var cell = IPython.notebook.get_selected_cell()
			var cell_text = cell.get_text();
			jupyter-notebook:copy-cell
			jupyter-notebook:paste-cell-below
			
		}
	
		var action =  {
		icon: 'fa-check-square', // a font-awesome class used on buttons, etc
        help    : 'chequear',
        help_index : 'zz',
        handler : handler
	}

    return {
        load_ipython_extension: check_extension
    };
});


