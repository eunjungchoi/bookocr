
//
function ensureImageLoad($img) {
    var dfd = $.Deferred();
    $img.on('load', function onImageLoad() {
        dfd.resolve();
    }).each(function onAlreadyLoaded() {
        if (this.complete) $(this).load();
    });
    return dfd.promise();
}

// temporarily disable zoom on tap
function temporarilyDisableZoomOnTap($el) {
    const is_iOS = navigator.userAgent.length && /iPhone|iPad|iPod/i.test(navigator.userAgent);

    if (!is_iOS) {
        return;
    }

    var $head = $('head');

    // if the device is an iProduct, apply the fix whenever the users touches an input
    $el
        .on('touchstart', () => disableZoom())
        .on('touchend', () => setTimeout(enableZoom, 500));

    // define a function to disable zooming
    function disableZoom() {
        $head.find('meta[name=viewport]').remove();
        $head.prepend('<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0" />');
    };

    // ... and another to re-enable it
    function enableZoom() {
        $head.find('meta[name=viewport]').remove();
        $head.prepend('<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=1" />');
    };
}

