
(function(root, factory) {
    if (typeof define === "function" && define.amd) {
        define("typebook.js", [ "jquery" ], function(a0) {
            return factory(a0);
        });
    } else if (typeof exports === "object") {
        module.exports = factory(require("jquery"));
    } else {
        factory(jQuery);
    }
})(this, function($) {

    var old = $.fn.typebook;
    $.fn.typebook = function() {
        var args = Array.prototype.slice.apply(arguments);
        args.unshift(this);
        return typebook.apply(typebook, args);
    };
    $.fn.typebook.noConflict = function() {
        $.fn.typebook = old;
        return this;
    };

    function typebook($el, googleApiKey) {
        //
        // 1. auth with GoogleApiKey
        //

        // insert google api initializer
        //
        //      function initGoogleApi() {
        //          gapi.client.setApiKey(googleApiKey);
        //          gapi.client.load('books', 'v1', function() {
        //              //console.log('load books api');
        //          });
        //      }
        //
        var handlerName = "initGoogleApi_" + Date.now();
        var initScriptEl = document.createElement('script');
        initScriptEl.type = "text/javascript";
        initScriptEl.innerText = [
            "function " + handlerName + "() {",
                "gapi.client.setApiKey(googleApiKey);",
                "gapi.client.load('books', 'v1', function() {",
                '});',
            "}",
        ].join('\n');
        document.getElementsByTagName("script")[0].parentNode.appendChild(initScriptEl);

        // insert google api client script
        var scriptEl = document.createElement('script');
        scriptEl.async = true;
        scriptEl.src = "https://apis.google.com/js/client.js?onload=" + 'initGoogleApi';
        document.getElementsByTagName("script")[0].parentNode.appendChild(scriptEl);

        //
        // 2. bind typeahead
        //

        // build google request bloodhound with GoogleApiKey
        var googleRequestUrl = 'https://content.googleapis.com/books/v1/volumes?key=' + googleApiKey + '&maxResults=20&orderBy=relevance&q=%QUERY';
        var googleBooks = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            //prefetch: '../data/films/post_1960.json',
            remote: {
                url: googleRequestUrl,
                wildcard: '%QUERY',
                //prepare: function(query, settings) {
                //    console.log('prepare:', query, settings);
                //    return settings;
                //},
                transform: transformGoogleApiResult,
                rateLimitBy: "debounce", // [debounce, throttle]
                rateLimitWait: 300,
            },
        });

        function transformGoogleApiResult(response) {
            var query  = $typebook.typeahead('val');

            var items0 = response.items;
                items1 = _.map(items0, function(item, i) {
                    return _.get(item, 'volumeInfo', {});
                });

            function buildQueryFilter(query) {
                return function (title) {
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
            var items = _.filter(items1, function(volume, i) {
                if (searchQuery(volume.title    ))  { return true }
                if (searchQuery(volume.subtitle ))  { return true }
                if (searchQuery(volume.publisher))  { return true }
                if (searchQuery((volume.authors||[]).join(' '))) { return true }
                //console.log(i, 'filter out:', volume.title, query0, volume.title.replace(/ /g, '').indexOf(query0));
                return false;
            });
            if (response.items.length !== items.length) {
                console.log('filtered:', items1.length, '=>', items.length);
            }
            //
            var result = _.map(items, function(volume, i) {
                //console.log(i, volume);
                var title    = volume.title;
                var subtitle = volume.subtitle;
                var authors  = volume.authors || [];
                var author1  = authors[0];
                var isbn13 = (_.find(_.get(volume, 'industryIdentifiers', []), function(ident) {
                    return ident.type === "ISBN_13";
                })||{}).identifier;
                var isbn10 = (_.find(_.get(volume, 'industryIdentifiers', []), function(ident) {
                    return ident.type === "ISBN_10";
                })||{}).identifier;
                var pageCount = volume.pageCount;
                var categories = volume.categories;
                var publisher = volume.publisher;
                var publishedDate = volume.publishedDate;
                var description = volume.description;
                var thumbnail = _.get(volume, 'imageLinks.thumbnail');
                var thumbnailSmall = _.get(volume, 'imageLinks.smallThumbnail');
                //
                var previewLink = volume.previewLink;
                var canonicalVolumeLink = volume.canonicalVolumeLink;

                //
                var subtitleStr = '';
                if (subtitle) {
                    subtitleStr += '- ' + subtitle;
                }
                var idStr    = 'typebook-result-item-' + i;
                var classStr = 'typebook-result-item';

                //
                return {
                    idStr: idStr,
                    classStr: classStr,
                    title      : title,
                    subtitle   : subtitle,
                    subtitleStr: subtitleStr,
                    authors  : authors,
                    author1  : author1,
                    authorsStr: authors.join(', '),
                    isbn     : isbn13,
                    publisher: publisher,
                    publishedDate: publishedDate,
                    thumbnail: thumbnailSmall || thumbnail,
                    //
                    previewLink: previewLink,
                    canonicalVolumeLink: canonicalVolumeLink,
                    //
                    //item : item,
                    value: title,
                };
            });
            return result;
        }


        // typeahead
        //var args = Array.prototype.slice.apply(arguments);
        //args.shift();
        //args.shift();
        //var $typebook = $el.typeahead.apply($el, args);
        var $typebook = $el.typeahead(null, {
            name: 'book',
            source: googleBooks,
            display: 'value',
            hint: true,
            templates: {
                //notFound: '<div class="empty-message">적당한 책을 찾을 수가 없습니다.</div>',
                empty: '<div class="empty-message">적당한 책을 찾을 수가 없습니다.</div>',
                pending: '<div class="pending-message">Searching... <i class="glyphicon glyphicon-refresh"></i></div>',
                suggestion: Handlebars.compile([
                    "<div href='{{canonicalVolumeLink}}' target='_blank' id='{{idStr}}' class='{{classStr}}'>",
                        "<div class='img-wrapper'>",
                            "<img class='thumbnail' src='{{thumbnail}}' />",
                        "</div>",
                        "<div class='book-info'>",
                            "<div class='first-row'>",
                                "<span class='book-title'>{{title}}</span>",
                                ", <span class='book-author'>{{ authorsStr }}</span>",
                                " <a href='{{canonicalVolumeLink}}' target='_blank' style='display: none;'>바로가기</a>",
                            "</div>",
                            "<div class='second-row'>",
                                "<span class='book-subtitle' title={{subtitleStr}}>{{subtitleStr}}</span>",
                            "</div>",
                            "<div class='third-row'>",
                                "<span class='book-publisher'>{{ publisher }}</span>",
                            "</div>",
                        "</div>",
                        "<div class='cleaner'></div>",
                    "</div>"
                ].join(""))
            }
        });

        $typebook.on('typeahead:select', function(ev, itemObj) {
            var $el   = $('#' + itemObj.idStr);
            var $link = $el.find('a');

            //
            window.open($link.attr('href'), '_blank');
        });

        return $typebook;
    }

});

