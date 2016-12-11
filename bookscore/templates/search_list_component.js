(function() {

  var SearchListComponent = (function() {

    var TEMPLATE = `
      <aside>
      <form class="search-form">
      <input name="search-input" type="text" />
      <input type="submit" value="검색" />
      </form>

      <div>
      <ul class="search-result-list">
      </ul>
      </div>
      </aside>
      `;
    var compiledTemplate = ejs.compile(TEMPLATE);

    var $el;

    function this$(...args) {
      if (!$el) {
        throw new Error('$el is not set.');
      }

      //
      var args = Array.prototype.slice.apply(arguments);
      return $el.find.apply($el, args);
    }

    function render($target) {
      // var html = ejs.render(templateStr, {data: 123});
      var html = compiledTemplate({data: 123});

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

    function bindHandleSearch(onSearchResult) {
      this$('.search-form').on('submit', function(ev) {
        ev.preventDefault();

        // request search
        var searchText = this$('input[name="search-input"]').val();
        requestSearch(searchText).then(function(data) {

          // handle search result
          var result = JSON.parse(data);
          renderSearchResults(result);

          //
          onSearchResult(result);
        });
      });
    }

    function renderSearchResults(result) {
      // prepare html
      var htmlList = result.channel.item.map(function(bookItem) {
        var template = '<li><%= title %></li>';
        var html = ejs.render(template, { title: bookItem.title });
        return html;
      });
      var html = htmlList.join('');

      // build DOM
      this$('.search-result-list').html(html);

    }

    function requestSearch(query) {
      // return $.ajax({
      //   method: 'get',
      //   url: 'http://localhost:8000',
      //   data: { q: query },
      // }).promise();

      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          resolve(`
            {
            	"channel": {
            		"result": "10",
            		"title": "Search Daum Open API",
            		"totalCount": "618",
            		"description": "Daum Open API search result",
            		"item": [{
            				"author_t": "존 스타인벡",
            				"sale_price": "8820",
            				"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788932909776%3Fmoddttm=20161104052232",
            				"sale_yn": "Y",
            				"pub_date": "20091130",
            				"link": "http://book.daum.net/detail/book.do?bookid=KOR9788932909776",
            				"barcode": "KOR9788932909776",
            				"etc_author": "윤희기 AU00367280",
            				"status_des": "정상판매",
            				"author": "존 스타인벡",
            				"title": "&lt;b&gt;의심스러운&lt;/b&gt; 싸움",
            				"category": "소설 ",
            				"translator": "윤희기",
            				"pub_nm": "열린책들",
            				"description": "1930년대 초 미국 리얼리즘 문학의 걸작! 고전들을 젊고 새로운 얼굴로 재구성한 전집「열린책들 세계문학」시리즈. 문학 거장들의 대표작은 물론 추리, 환상, SF 등 장르 문학의 ...",
            				"isbn": "8932909776",
            				"ebook_barcode": "DGT00018304756IN",
            				"isbn13": "9788932909776",
            				"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788932909776%3Fmoddttm=20161104052232",
            				"list_price": "9800"
            			}, {
            				"author_t": "존 스타인벡",
            					"sale_price": "3000",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788932906362%3Fmoddttm=20150223142547",
            					"sale_yn": "Y",
            					"pub_date": "20060225",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR9788932906362",
            					"barcode": "KOR9788932906362",
            					"etc_author": "윤희기  존 스타인벡  존스타인벡",
            					"status_des": "정상판매",
            					"author": "존 스타인벡",
            					"title": "&lt;b&gt;의심스러운&lt;/b&gt; 싸움(페이퍼북)",
            					"category": "소설 ",
            					"translator": "윤희기",
            					"pub_nm": "열린책들",
            					"description": "노벨 문학상 수상 작가인 존 스타인백의 첫 정치 소설 『의심스러운 싸움』. 1930년대 대공황기 캘리포니아 농장 지대의 파업을 아름다운 문장으로 그려내고 있다. 번역자의 말과 ...",
            					"isbn": "893290636X",
            					"ebook_barcode": "",
            					"isbn13": "9788932906362",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788932906362%3Fmoddttm=20150223142547",
            					"list_price": "7800"
            			}, {
            				"author_t": "존 스타인벡",
            					"sale_price": "3600",
            					"cover_s_url": "",
            					"sale_yn": "N",
            					"pub_date": "19900601",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR2004613001452",
            					"barcode": "KOR2004613001452",
            					"etc_author": "윤희기  존 스타인벡  존스타인벡",
            					"status_des": "",
            					"author": "존 스타인벡",
            					"title": "&lt;b&gt;의심스러운&lt;/b&gt; 싸움",
            					"category": "소설 ",
            					"translator": "윤희기",
            					"pub_nm": "열린책들",
            					"description": "",
            					"isbn": "",
            					"ebook_barcode": "",
            					"isbn13": "2004613001452",
            					"cover_l_url": "",
            					"list_price": "4000"
            			}, {
            				"author_t": "존 스타인벡",
            					"sale_price": "0",
            					"cover_s_url": "",
            					"sale_yn": "N",
            					"pub_date": "19900601",
            					"link": "http://book.daum.net/detail/book.do?bookid=BOK0001661055611",
            					"barcode": "BOK0001661055611",
            					"etc_author": "윤희기",
            					"status_des": "",
            					"author": "존 스타인벡",
            					"title": "&lt;b&gt;의심스러운&lt;/b&gt; 싸움",
            					"category": "",
            					"translator": "윤희기",
            					"pub_nm": "열린책들",
            					"description": "백화점 포장계장으로 일하는 짐은 우연히 공산당 집회를 구경하다가 붙잡혀 부랑죄를 뒤집어쓴다. 풀려나자 그는 공산당에 가입, 농장 파업에 참여하게 되나 결국 죽음을 맞게 되는데...",
            					"isbn": "2000977421",
            					"ebook_barcode": "",
            					"isbn13": "9782000977421",
            					"cover_l_url": "",
            					"list_price": "4000"
            			}, {
            				"author_t": "울프리드 노이만",
            					"sale_price": "11700",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788974649524%3Fmoddttm=20161117060511",
            					"sale_yn": "Y",
            					"pub_date": "20141231",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR9788974649524",
            					"barcode": "KOR9788974649524",
            					"etc_author": "김학태",
            					"status_des": "정상판매",
            					"author": "울프리드 노이만",
            					"title": "법과 진리",
            					"category": "정치/사회 ",
            					"translator": "김학태",
            					"pub_nm": "한국외국어대학교출판부",
            					"description": "이 책은 법에서 진리(정당성)의 가능성을 둘러싸고 철학적 사유를 전개해야 할 뿐만 아니라, 법과 법학에서 제기되는 진리주장의 실천적 의미에 대해서도 탐구해야 한다는 사실을 기본적...",
            					"isbn": "8974649527",
            					"ebook_barcode": "",
            					"isbn13": "9788974649524",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788974649524%3Fmoddttm=20161117060511",
            					"list_price": "13000"
            			}, {
            				"author_t": "셸리 케이건",
            					"sale_price": "15120",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FBOK00019386267BA%3Fmoddttm=20161120060411",
            					"sale_yn": "Y",
            					"pub_date": "20121121",
            					"link": "http://book.daum.net/detail/book.do?bookid=BOK00019386267BA",
            					"barcode": "BOK00019386267BA",
            					"etc_author": "박세연 AU01077882",
            					"status_des": "정상판매",
            					"author": "셸리 케이건",
            					"title": "죽음이란 무엇인가",
            					"category": "인문 ",
            					"translator": "박세연",
            					"pub_nm": "엘도라도",
            					"description": "\u2018JUSTICE\u2019·\u2018HAPPINESS\u2019에 이은 아이비리그 3대 명강 \u2018DEATH\u2019★ 나는 \u2018반드시\u2019 죽을 것이다 그렇다면 나는 \u2018어떻게\u2019 살아야 하는가? 17년 연속 예일대 최고의 명강의 \u2018DEATH\u2019가 책으로...",
            					"isbn": "8901152215",
            					"ebook_barcode": "DGT4808901152219",
            					"isbn13": "9788901152219",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FBOK00019386267BA%3Fmoddttm=20161120060411",
            					"list_price": "16800"
            			}, {
            				"author_t": "박상효",
            					"sale_price": "12600",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FBOK00010041421AL%3Fmoddttm=20161120060411",
            					"sale_yn": "Y",
            					"pub_date": "20100405",
            					"link": "http://book.daum.net/detail/book.do?bookid=BOK00010041421AL",
            					"barcode": "BOK00010041421AL",
            					"etc_author": "",
            					"status_des": "정상판매",
            					"author": "박상효",
            					"title": "영문법 콘서트",
            					"category": "외국어 ",
            					"translator": "",
            					"pub_nm": "잉글리시팩토리",
            					"description": "영문법의 기본 개념들을 잡아주는 친절한 문법책 인터넷에서 시리즈 동영상 강의로 유명한 박상효 선생님의 영문법 개념잡이 책이다. 영어 문법의 기초적인 개념과 용법을 이야기식으로...",
            					"isbn": "8931518579",
            					"ebook_barcode": "",
            					"isbn13": "9788931518573",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FBOK00010041421AL%3Fmoddttm=20161120060411",
            					"list_price": "14000"
            			}, {
            				"author_t": "팀 데도풀로스",
            					"sale_price": "10620",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788963221083%3Fmoddttm=20161120090706",
            					"sale_yn": "Y",
            					"pub_date": "20161021",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR9788963221083",
            					"barcode": "KOR9788963221083",
            					"etc_author": "박미영",
            					"status_des": "정상판매",
            					"author": "팀 데도풀로스",
            					"title": "뇌가 섹시해지는 추리퀴즈(1단계)",
            					"category": "자기계발 ",
            					"translator": "박미영",
            					"pub_nm": "비전코리아",
            					"description": "추리소설 마니아부터 추리작가 지망생까지, 전폭적 지지를 받고 있는 팀 데도풀로스의 최신작! 100여 년 전부터 영국과 유럽에서는 추리소설 읽기가 품위 있는 신사의 대표적인 취미...",
            					"isbn": "8963221083",
            					"ebook_barcode": "DGT4808963221083",
            					"isbn13": "9788963221083",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788963221083%3Fmoddttm=20161120090706",
            					"list_price": "11800"
            			}, {
            				"author_t": "김려령",
            					"sale_price": "9900",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788936433635%3Fmoddttm=20161117060511",
            					"sale_yn": "Y",
            					"pub_date": "20080321",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR9788936433635",
            					"barcode": "KOR9788936433635",
            					"etc_author": "",
            					"status_des": "정상판매",
            					"author": "김려령",
            					"title": "완득이",
            					"category": "소설 ",
            					"translator": "",
            					"pub_nm": "창비",
            					"description": "차차차보다 유쾌하게, 킥복싱보다 통쾌하게! 마해송문학상과 문학동네 어린이문학상, 창비청소년문학상을 석권한 김려령 신작 소설. 집도 가난하고 공부도 못하지만 싸움만큼은 누...",
            					"isbn": "8936433636",
            					"ebook_barcode": "DGT00021199511BA",
            					"isbn13": "9788936433635",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788936433635%3Fmoddttm=20161117060511",
            					"list_price": "11000"
            			}, {
            				"author_t": "김려령",
            					"sale_price": "8550",
            					"cover_s_url": "http://t1.daumcdn.net/thumb/R72x100/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788936456085%3Fmoddttm=20161120060411",
            					"sale_yn": "Y",
            					"pub_date": "20140317",
            					"link": "http://book.daum.net/detail/book.do?bookid=KOR9788936456085",
            					"barcode": "KOR9788936456085",
            					"etc_author": "",
            					"status_des": "정상판매",
            					"author": "김려령",
            					"title": "완득이",
            					"category": "소설 ",
            					"translator": "",
            					"pub_nm": "창비",
            					"description": "차차차보다 유쾌하게, 킥복싱보다 통쾌하게! 마해송문학상과 문학동네 어린이문학상, 창비청소년문학상을 석권한 김려령 신작 소설. 집도 가난하고 공부도 못하지만 싸움만큼은 누...",
            					"isbn": "8936456083",
            					"ebook_barcode": "DGT00019807263AL",
            					"isbn13": "9788936456085",
            					"cover_l_url": "https://t1.search.daumcdn.net/thumb/R110x160/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fbook%2FKOR9788936456085%3Fmoddttm=20161120060411",
            					"list_price": "9500"
            			}],
            			"lastBuildDate": "Sun, 20 Nov 2016 18:14:16 +0900",
            			"link": "http://dna.daum.net/apis",
            			"generator": "Daum Open API"
            	}
            }
            	          `);
        }, 300);
      });
    }

    //
    function runner($clickable, onSearchResult) {
      $el = render($('#sidebar'));

      //
      // bindChangeBackgroundColorOnClick($clickable);
      bindHandleSearch(onSearchResult);
    };

    return runner;
  })();

  xport('search_list_component.js',  SearchListComponent);

})();
