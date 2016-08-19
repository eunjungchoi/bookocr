/* global $, Cropper, autosize */

function initCropper($img, $parent) {
    // cropper
    var cropper = new Cropper();
    $parent.data('cropper', cropper);

    // getOriginalWidthOfImg
    //  see http://stackoverflow.com/questions/318630/get-real-image-width-and-height-with-javascript-in-safari-chrome
    var _img = new Image();
    _img.src = $img.attr('src');
    $img.data('original-width',  _img.width);
    $img.data('original-height', _img.height);

    // init
    var width  = $img.width(),
        height = $img.height();
    var fullSize = { w: width, h: height };
    cropper.init($parent, null, null, fullSize);

    return cropper;
}

function bindCropperWithOCR(cropper, url, {
    $wrap,
    $img,
    $toolbar,
    $form,
    $cropInfo,
    $ocrButton,
}, onPostResult) {
    var dfd = $.Deferred();

    // $ocrButton
    var _isSaving = false;
    $ocrButton.on('click', function onClickRecognize(ev) {
        ev.preventDefault();
        if (_isSaving) return;

        // form data
        var imageCropData = $form.serializeArray().reduce((memo, obj) => {
            return Object.assign({}, memo, {
                [obj.name]: obj.value,
            });
        }, {});
        // re-noramlize with image original size
        imageCropData['crop-x'] = parseInt(parseFloat(imageCropData['crop-x']) / $img.width()  * $img.data('original-width' ), 10);
        imageCropData['crop-y'] = parseInt(parseFloat(imageCropData['crop-y']) / $img.height() * $img.data('original-height'), 10);
        imageCropData['crop-w'] = parseInt(parseFloat(imageCropData['crop-w']) / $img.width()  * $img.data('original-width' ), 10);
        imageCropData['crop-h'] = parseInt(parseFloat(imageCropData['crop-h']) / $img.height() * $img.data('original-height'), 10);

        // POST
        var pr = postOCR(imageCropData, url);

        // enable/disable $ocrButton
        _isSaving = true;
        $ocrButton.button('loading');
        pr.then(null).then(function () {
            $ocrButton.button('reset');
            _isSaving = false;
        });

        pr.then(onPostResult);
    });

    //
    // bind cropper events

    //cropper.on('select:start', function onSelectStart(ev, x,y,w,h) {});
    //cropper.on('release', function onSelectRelease() {});

    // update crop rect info on select
    cropper.on('select', function updateCropRectInfo(ev, x, y, w, h) {
        // update crop-rect info
        $form
            .find('input[name="crop-x"]').val(x).end()
            .find('input[name="crop-y"]').val(y).end()
            .find('input[name="crop-w"]').val(w).end()
            .find('input[name="crop-h"]').val(h).end();

        var cropInfoText = `x ${x} y ${y} w ${w} h ${h}`;
        $cropInfo
            .text(cropInfoText)
            .attr('title', cropInfoText)
        ;
    });

    // show/hide toolbar during change/select
    cropper.on('change', function hideCropToolbar(ev, x,y,w,h) {
        $toolbar.hide();
    });
    cropper.on('select', function showCropToolbar(ev) {
        $toolbar.show()
            .appendTo(cropper.$selection());
    });

    return dfd.promise();
}

function postOCR(imageCropData, url) {
    return $.ajax({
        method: 'post',
        url: url,
        data: imageCropData,
    });
}

function ensureImageLoad($img) {
    var dfd = $.Deferred();
    $img.on('load', function onImageLoad() {
        dfd.resolve();
    }).each(function onAlreadyLoaded() {
        if (this.complete) $(this).load();
    });
    return dfd.promise();
}

///
function initCrop(postUrl, elements) {
    const {
        $img,
        $wrap,
        $toolbar,
        $form,
        $cropInfo,
        $ocrButton,
        $textarea,
    } = elements;

    //
    autosize($textarea);

    ensureImageLoad($img).then(function () {
        // show cropper
        var cropper = initCropper($img, $wrap);

        // bind ocr
        bindCropperWithOCR(cropper, postUrl, elements, function writeOCRText(ocrResult) {
            const text = (ocrResult.result.text||'').replace(/\n/g, '') + "\n";
            $textarea.val(text);

            // resize textarea
            autosize.update($textarea);

            // focus
            $textarea[0].focus();
        });

        // select default area
        const width  = $img.width(),
              height = $img.height();
        const selectRect = { // blindly select (15~-15%, 25~-25%)
            x: width  * 0.15,
            w: width  * (1 - (0.15) * 2),
            y: height * 0.25,
            h: height * (1.0 - (0.25) * 2),
        };
        cropper.select(selectRect);
    });
}

