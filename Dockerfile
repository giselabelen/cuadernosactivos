RUN set -x \
  && jupyter contrib nbextension install --system \
  && jupyter nbextension enable --py --sys-prefix widgetsnbextension \
  && jupyter nbextensions_configurator enable --system \
  && jupyter nbextension enable addbefore/main --system \
  && jupyter nbextension enable autoscroll/main --system \
  && jupyter nbextension enable contrib_nbextensions_help_item/main --system \
  && jupyter nbextension enable datestamper/main --system \
  && jupyter nbextension enable dragdrop/main --system \
  && jupyter nbextension enable execute_time/ExecuteTime --system \
  && jupyter nbextension enable help_panel/help_panel --system \
  && jupyter nbextension enable hide_input/main --system \
  && jupyter nbextension enable highlighter/highlighter --system \
  && jupyter nbextension enable init_cell/main --system \
  && jupyter nbextension enable move_selected_cells/main --system \
  && jupyter nbextension enable notify/notify --system \
  && jupyter nbextension enable printview/main --system \
  && jupyter nbextension enable rubberband/main --system \
  && jupyter nbextension enable scroll_down/main --system \
  && jupyter nbextension enable search-replace/main --system \
  && jupyter nbextension enable table_beautifier/main --system \
  && jupyter nbextension enable toc2/main --system \
  && jupyter nbextension enable toggle_all_line_numbers/main --system;
