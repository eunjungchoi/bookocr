
//
// from https://developers.daum.net/services/apis/search/book
//

function DaumBook(apiKey, options) {
    this.apiKey = apiKey;

    // https://apis.daum.net/search/book?apikey=${apikey}&q=flask&output=json&sort=accu
    // https://apis.daum.net/search/book?q=%s&output=json&apikey=${apikey}
    // 'https://apis.daum.net/search/book?q=%s&output=json&sort=accu&apikey=' + this.apiKey
    var requestUrl = 'https://apis.daum.net/search/book?q=%s&output=json&sort=accu&apikey=' + this.apiKey;

    options = _.assign({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //prefetch: '../data/films/post_1960.json',
        remote: {
            url: requestUrl,
            ajax: { 
                jsonp: 'callback',
                dataType: 'jsonp',
            },
            //prepare: function(query, settings) {
            //    console.log('prepare:', query, settings);
            //    return settings;
            //},
            prepare: this.prepare.bind(this),
            transform: this.transform.bind(this),
            rateLimitBy: "debounce", // [debounce, throttle]
            rateLimitWait: 300,
            
            transport: function ajax(options, onSuccess, onError) {
                options = _.assign({}, {
                    success: onSuccess,
                    error: onError,
                }, options, { 
                    dataType: 'jsonp',
                });
                return $.ajax.apply($, arguments);
            },
        },
    }, options);

    //
    Bloodhound.call(this, options);
}

DaumBook.prototype = _.create(Bloodhound.prototype);

DaumBook.prototype.prepare = function(query, settings) {
    this.query   = query;
    settings.dataType = 'jsonp';
    settings.url = settings.url.replace('%s', encodeURIComponent(query));

    return settings;
};

DaumBook.prototype.transform = function(response) {
    var query = this.query;

    var volumes = _.map(response.channel.item);

    //
    function buildQueryFilter(query) {
        return function(title) {
            if (!title) {
                return false;
            }

            // case-insensitive
            title = title.toLowerCase();
            query = query.toLowerCase();

            // whitespace-insensitive
            title = title.replace(/ /g, '');
            query = query.replace(/ /g, '');

            return title.indexOf(query) !== -1;
        }
    }
    var searchQuery = buildQueryFilter(query);

    // filter
    var volumes = _.filter(volumes, function(volume, i) {
        if (searchQuery(volume.title))  { return true }
        if (searchQuery(volume.pub_nm)) { return true }
        if (searchQuery(volume.author_t)) { return true }
        //console.log(i, 'filter out:', volume.title, query0, volume.title.replace(/ /g, '').indexOf(query0));
        return false;
    });
    if (response.channel.item.length !== volumes.length) {
        ///console.log('filtered:', response.channel.item.length, '=>', volumes.length);
    }
    //
    var result = _.map(volumes, function(volume, i) {
        //console.log(i, volume);
        var title = volume.title.replace('&lt;b&gt;', '').replace('&lt;/b&gt;', '');

        var authors = [
            volume.author_t,
            volume.translator,
            volume.etc_author,
        ];
        authors = _.filter(authors, function(author) {
            return author;
        });

        var author1 = authors[0];
        var isbn13  = volume.isbn13;
        var publisher = volume.pub_nm;
        var publishedDate = volume.pub_date;
        var description = volume.description;
        var thumbnail      = volume.cover_l_url;
        var thumbnailSmall = volume.cover_s_url;
        //
        var idStr    = 'typebook-result-item-' + i;
        var classStr = 'typebook-result-item';

        //
        return {
            idStr: idStr,
            classStr: classStr,
            title      : title,
            subtitle   : '',
            subtitleStr: '',
            authors  : authors,
            author1  : author1,
            authorsStr: authors.join(', '),
            isbn     : isbn13,
            isbn13   : isbn13,
            publisher: publisher,
            publishedDate: publishedDate,
            thumbnail: thumbnailSmall || thumbnail,
            //
            value: title,
        };
    });
    ///console.log('transform', result.length, 'results.');
    return result;
};

