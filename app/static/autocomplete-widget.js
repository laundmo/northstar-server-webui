function AutocompleteTextWidget(lona_window) {
  this.lona_window = lona_window;

  this.setup = function () {
    // gets called when the widget gets initialized

    console.log("setup", this.nodes);
  };

  this.deconstruct = function () {
    // gets called when the widget gets destroyed

    console.log("deconstruct", this.nodes);
  };

  this.data_updated = function () {
    $(this.data[0]).autocomplete({
      source: this.data[1],
      minLength: 0,
    });
  };
}

Lona.register_widget_class("AutocompleteTextWidget", AutocompleteTextWidget);
