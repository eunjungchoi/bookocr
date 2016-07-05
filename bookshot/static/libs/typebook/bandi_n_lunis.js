
// http://222.122.120.242:7570/ksf/api/search?callback=jQuery1111024633783263541975_1467734777981&sn=product&q=%EC%8A%A4%ED%86%A0%EB%84%88&s=&l=20&o=0&pq=&ud=%7C%7C%7C&pt=&ct=&ps=&egp=09&inp=&_=1467734777982

var requestUrl = 'http://222.122.120.242:7570/ksf/api/search?callback=jQuery1111024633783263541975_1467734777981&sn=product&s=&l=20&o=0&pq=&ud=%7C%7C%7C&pt=&ct=&ps=&egp=09&inp=&_=1467734777982&q=%s';

function buildUrl(query) {
    return `http://222.122.120.242:7570/ksf/api/search?sn=product&s=&l=20&o=0&pq=&ud=%7C%7C%7C&pt=&ct=&ps=&egp=09&inp=&q=${encodeURIComponent(query)}`;
}

function BandiNLunis(options) {

    options = _.assign({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //prefetch: '../data/films/post_1960.json',
        remote: {
            url: requestUrl,
            prepare: this.prepare.bind(this),
            transform: this.transform.bind(this),
            rateLimitBy: "debounce", // [debounce, throttle]
            rateLimitWait: 300,
            //
            //transport: function ajax(options) {
            //    options = _.assign({}, options, { dataType: 'jsonp' });
            //    return $.ajax.apply($, arguments);
            //},
        },
    }, options);

    //
    Bloodhound.call(this, options);
}
BandiNLunis.prototype = _.create(Bloodhound.prototype);

// override
BandiNLunis.prototype.initialize = function() {

    // auth
    authorize(this.apiKey);

    return Bloodhound.prototype.initialize.apply(this, arguments);
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

function stripTag(htmlStr) {
    //var container = document.createElement('div');
    //var text = document.createTextNode(dirtyString);
    //container.appendChild(text);
    //return container.innerHTML; // innerHTML will be a xss safe string

    return htmlStr.replace(/(<([^>]+)>)/ig, "");
}

BandiNLunis.prototype.prepare = function(query, settings) {
    this.query = query;

    settings.url      = buildUrl(query);
    settings.dataType = 'jsonp';

    return settings;
};


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
BandiNLunis.prototype.transform = function(response) {
    var query = this.query;

    //console.log('response:', response);

    var count   = response.count;
    var volumes = response.result;

    // map
    volumes = _.map(volumes, function(volume, i) {
        //console.log(i, volume);
        var title = volume.prod_name;
            title = stripTag(title);
        //console.log(volume.prod_name, title);

        var subtitle = volume.buje;
            subtitle = stripTag(subtitle);

        var authors = [
            volume.author,
            volume.translator
        ].filter(function(x) { return x });
        var author1 = authors[0];

        var isbn = volume.isbn || volume.barcode;

        //var pageCount = volume.pageCount;
        //var categories = volume.categories;

        var publisher = volume.maker;
            publisher = stripTag(publisher);
        var publishedDate = volume.pdate

        var description = volume.contents_description;
            description = stripTag(description);

        var thumbnail = 'http://image.bandinlunis.com/upload' + volume.prod_img;

        //
        var isDomestic = volume.prod_type === '01';
        var isAlbum    = volume.prod_type === '03';
        var isGift     = volume.prod_type === '04';
        var isUsed     = volume.prod_type === '05';
        var isEbook    = volume.prod_type === '06';
        var isDVD      = volume.prod_type === '07';
        var isAbroad   = volume.prod_type === '08';

        //
        if (isEbook) {
            title = '[eBook] ' + title;
        }

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
            isbn     : isbn,
            publisher: publisher,
            publishedDate: publishedDate,
            thumbnail: thumbnail,

            //
            isDomestic: isDomestic,
            isAlbum   : isAlbum,
            isGift    : isGift,
            isUsed    : isUsed,
            isEbook   : isEbook,
            isDVD     : isDVD,
            isAbroad  : isAbroad,

            value: title,
        };
    });

    // filter out other media
    volumes = _.filter(volumes, function(volume, i) {
        return !volume.isAlbum && !volume.isGift && !volume.isUsed && !volume.isDVD;
    });

    // filter once again by query
    var searchQuery = buildQueryFilter(query);
    volumes = _.filter(volumes, function(volume, i) {
        if (searchQuery(volume.title    ))  { return true }
        if (searchQuery(volume.subtitle ))  { return true }
        if (searchQuery(volume.publisher))  { return true }
        if (searchQuery((volume.authors||[]).join(' '))) { return true }
        //console.log(i, 'filter out:', volume.title, query0, volume.title.replace(/ /g, '').indexOf(query0));
        return false;
    });
    if (count !== volumes.length) {
        console.log('filtered:', count, '=>', volumes.length);
        //console.log(volumes1);
        //console.log(volumes);
    }


    //
    return volumes;
};


