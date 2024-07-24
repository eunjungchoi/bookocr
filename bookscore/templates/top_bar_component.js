(function() {

  var TopBarComponent = (function() {
    var TEMPLATE = `
    <button class="search-btn"><i class="fa fa-search" aria-hidden="true"></i></button>
    <button class="close-search-btn"><i class="fa fa-close" aria-hidden="true"></i></button>
    `;

    function render($target) {
      var html = ejs.render(TEMPLATE);
      $target.html(html);

      return $($target.children()[0]);
    }

    return function (onClickSearchButton, onClickSearchCloseButton) {
      render($('#topbar'))

      $('#topbar .search-btn').on('click', onClickSearchButton);
      $('#topbar .close-search-btn').on('click', onClickSearchCloseButton);
    };

  })();

  //
  xport('top_bar_component.js',  TopBarComponent);

})();
