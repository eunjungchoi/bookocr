
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
    // jQuery
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

    //
    var $typebook;
    function typebook($el, options, datasets) {
        // build engine
        var Engine = $.fn.typebook.engines[options['engine']];
        var apiKey = options['apiKey'];
        var engine = new Engine(apiKey);

        // 1. authorize
        engine.init();

        // 2. typeahead
        //var args = Array.prototype.slice.apply(arguments);
        //args.shift();
        //args.shift();
        //var $typebook = $el.typeahead.apply($el, args);
        $typebook = $el.typeahead(options, _.assign({
            name: 'book',
            source: engine.source({ $typebook: $($el) }),
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
        }, datasets));

        // bind click
        $typebook.on('typeahead:select', function(ev, itemObj) {
            var $el   = $('#' + itemObj.idStr);
            var $link = $el.find('a');

            //
            window.open($link.attr('href'), '_blank');
        });

        return $typebook;
    }

});

