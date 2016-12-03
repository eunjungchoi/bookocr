var SearchListComponent = (function() {

  const TEMPLATE = `
    <aside>
    <form class="search-form">
    <input type="text" />
    <input type="submit" value="검색" />
    </form>

    <div>
    <ul>
    </ul>
    </div>
    </aside>
    `;

  var $el;

  function render(templateStr, $target) {
    var html = ejs.render(templateStr)

    $target.html(html);

    return $($target.children()[0]);
  }


  function bindChangeBackgroundColorOnClick($someClickableElement) {
    // XXX temporary
    var clickCount = 0;
    var colors = ['white', 'blue', 'red', 'yellow'];
    $someClickableElement.on('click', '.search-btn', function() {
      clickCount += 1;
      $el.css('background-color', colors[clickCount % 4]);
    });
  }

  function bindHandleSearch() {
    //
    $el.find('.search-form').on('submit', function(ev) {
      ev.preventDefault();

      console.log('search:', ev);
    });
  }

  //
  function runner($clickable) {
    $el = render(TEMPLATE, $('#sidebar'));

    //
    bindChangeBackgroundColorOnClick($clickable);
    bindHandleSearch();
  };

  return runner;
})();
