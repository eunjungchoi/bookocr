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

function bindCropperWithOCR(cropper, $wrap, $img, onOCR) {
    var dfd = $.Deferred();

    //
    var $toolbar = $wrap.find('.crop-tool-layer');
    var $form = $('form[name="ocr-form"]');
    var $cropInfo = $toolbar.find('.crop-info'),
        $saveBtn = $toolbar.find('button[name="ocr"]')
    ;

    // $saveBtn
    var _isSaving = false;
    $saveBtn.on('click', function(ev) {
        ev.preventDefault();
        if (_isSaving) { return }

        // form data
        var imageCropData = $form.serializeArray().reduce((memo, obj) => {
            memo[obj.name] = obj.value;
            return memo;
        }, {});
        // re-noramlize with image original size
        imageCropData['crop-x'] = parseInt(parseFloat(imageCropData['crop-x']) / $img.width()  * $img.data('original-width' ));
        imageCropData['crop-y'] = parseInt(parseFloat(imageCropData['crop-y']) / $img.height() * $img.data('original-height'));
        imageCropData['crop-w'] = parseInt(parseFloat(imageCropData['crop-w']) / $img.width()  * $img.data('original-width' ));
        imageCropData['crop-h'] = parseInt(parseFloat(imageCropData['crop-h']) / $img.height() * $img.data('original-height'));

        // POST
        var pr = postOCR(imageCropData);

        _isSaving = true;
        $saveBtn.button('loading');

        pr.then(function(ocrResult) {
            _isSaving = false;
            $saveBtn.button('reset')
            //
            dfd.resolve(ocrResult);
        }, function(err) {
            _isSaving = false;
            $saveBtn.button('reset')
            dfd.reject(err);
        });
    });

    //
    // bind cropper events
    //
    cropper.on('change', function(ev, x,y,w,h) {
        $toolbar.hide();
    });
    cropper.on('select:start', function(ev, x,y,w,h) {});
    cropper.on('release', function() {});

    cropper.on('select', function(ev, x,y,w,h) {
        var $selection = cropper.$selection();

        // update crop-rect info
        $form
            .find('input[name="crop-x"]').val(x).end()
            .find('input[name="crop-y"]').val(y).end()
            .find('input[name="crop-w"]').val(w).end()
            .find('input[name="crop-h"]').val(h).end();

        var cropInfoText = `x ${x} y ${y} w ${w} h ${h}`;
        $cropInfo.attr('title', cropInfoText).text(cropInfoText);

        //
        $toolbar
            .show()
            .appendTo($selection);
    });

    return dfd.promise();
}

function postOCR(imageCropData) {
    return $.ajax({
        method: 'post',
        url: "{% url 'post_quote_ocr' book_id=book.id quote_id=quote.id %}",
        data: imageCropData,
    });

}


///
$(function() {
    var $img = $('.image-preview-container img.obj');

	// image loaded
	(function() {
		var dfd = $.Deferred();
		$img.on('load', function() {
			dfd.resolve();
		}).each(function() {
			if (this.complete) { $(this).load() }
		});
		return dfd.promise();
	})()
	.then(function() {
		// show cropper
		var $_wrapper = $img.parent();
		var cropper = initCropper($img, $_wrapper);

        // bind ocr
        var $textarea = $('textarea[name="quotation"]');
        bindCropperWithOCR(cropper, $_wrapper, $img).then(function(ocrResult) { 
            //console.log(ocrResult);
            $textarea.val(ocrResult.result.text);
            $textarea[0].focus();
        }, function(err) { 
            console.error(err);
        });

        // select default area
        var width  = $img.width(),
            height = $img.height();
        var selectRect = { // blindly select (15~-15%, 25~-25%)
            x: width * 0.15, 
            w: width * (1 - (0.15)*2),
            y: height * 0.25,
            h: height * (1.0 - (0.25)*2),
        };
        cropper.select(selectRect);
	});
});