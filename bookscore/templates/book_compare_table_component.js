(function() {

  var BookCompareTableComponent = (function() {

  function buildRowHtml(data) {
    var template = `
      <tr>
          <td><%= title %></td>
          <td><%= authors %></td>
          <td><%= pages %></td>
          <td><%= ebook || "" %></td>
          <td><%= scores.goodreads %></td>
          <td><%= scores.amazon %></td>
          <td><%= scores.aladin %></td>
          <td><%= scores.kyobo %></td>
          <td><%= scores.yes24 %></td>
      </tr>
    `;


    var html = ejs.render(template, data);
    return html;
  }

  return function renderTable($target, data) {
      var totalTemplate = `<table class="table table-striped <%= classname %>">
        <thead>
            <tr>
                <th>제목</th>
                <th>저자</th>
                <th>쪽수</th>
                <th>ebook</th>
                <th>goodreads</th>
                <th>amazon</th>
                <th>aladin</th>
                <th>kyobo</th>
                <th>yes24</th>
            </tr>
        </thead>
        <tbody>
          ${data.map(function(bookInfo) {
            return buildRowHtml(bookInfo);
          }).join('')}
        </tbody>
      </table>`;

      //
      var html = ejs.render(totalTemplate, { classname: 'book-compare-table' });
      $target.html(html);
    }
  })();

  //
  xport('book_compare_table_component.js',  BookCompareTableComponent);
})();
