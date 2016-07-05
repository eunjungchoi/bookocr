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

    function GoogleBooksEngine(apiKey) {
        this.apiKey = apiKey;
    }

    GoogleBooksEngine.prototype.init = function() {
        this.auth();
    };

    function insertScript(attrs) {
        attrs = attrs || {};

        var scriptEl = document.createElement('script');
        for(var key in attrs) {
            scriptEl[key] = attrs[key];
        }

        document.getElementsByTagName("script")[0].parentNode.appendChild(scriptEl);
    }
    function insertScriptSrc(src, attrs) {
        attrs = attrs || {};
        attrs['src'] = src;

        return insertScript(attrs);
    }

    GoogleBooksEngine.prototype.auth = function() {
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
        var innerText = [
            "function " + handlerName + "() {",
                "gapi.client.setApiKey('" + this.apiKey + "');",
                "gapi.client.load('books', 'v1', function() {",
                '});',
            "}",
        ].join('\n');
        insertScript({type: 'text/javascrpt', innerText: innerText});

        // insert google api client script
        if (typeof gapi === 'undefined' || typeof (gapi||{})['client'] === 'undefined') {
            insertScriptSrc("https://apis.google.com/js/client.js?onload=" + 'initGoogleApi', { async: true });
        }
    };

    var DEFAULT_IMAGE_COVER = 'https://www.google.com/googlebooks/images/no_cover_thumb.gif';

    GoogleBooksEngine.prototype.transform = function(response) {
        var query = this.$typebook.typeahead('val');

        var volumes1 = _.map(response.items, function(item, i) {
            return _.get(item, 'volumeInfo', {});
        });

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
        var volumes = _.filter(volumes1, function(volume, i) {
            if (searchQuery(volume.title    ))  { return true }
            if (searchQuery(volume.subtitle ))  { return true }
            if (searchQuery(volume.publisher))  { return true }
            if (searchQuery((volume.authors||[]).join(' '))) { return true }
            //console.log(i, 'filter out:', volume.title, query0, volume.title.replace(/ /g, '').indexOf(query0));
            return false;
        });
        if (response.items.length !== volumes.length) {
            console.log('filtered:', volumes1.length, '=>', volumes.length);
            //console.log(volumes1);
            //console.log(volumes);
        }
        //
        var result = _.map(volumes, function(volume, i) {
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
                thumbnail: thumbnailSmall || thumbnail || DEFAULT_IMAGE_COVER,
                //
                previewLink: previewLink,
                canonicalVolumeLink: canonicalVolumeLink,
                //
                //item : item,
                value: title,
            };
        });
        return result;
    };

    GoogleBooksEngine.prototype.source = function(options) {
        this.$typebook = options.$typebook;

        //var googleRequestUrl = 'https://content.googleapis.com/books/v1/volumes?key=' + this.apiKey + '&maxResults=20&orderBy=relevance&q=%QUERY';
        var googleRequestUrl = 'https://content.googleapis.com/books/v1/volumes?maxResults=20&orderBy=relevance&q=%QUERY';
        var googleBooksBloodHound = new Bloodhound(_.assign({
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
                transform: this.transform.bind(this),
                rateLimitBy: "debounce", // [debounce, throttle]
                rateLimitWait: 300,
            },
        }, options));

        return googleBooksBloodHound;
    };

    //
    $.fn.typebook.engines = $.fn.typebook.engines || {};
    $.fn.typebook.engines['GoogleBooks'] = GoogleBooksEngine;
});

