define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function check_extension() {

        var handler = function () {
            //alert('this is an alert from my new extension!');
            Jupyter.notebook.copy_cell();
			Jupyter.notebook.paste_cell_below();

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
