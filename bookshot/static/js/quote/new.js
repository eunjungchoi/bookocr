// handle file change
function handleFiles(files) {
	if (!files || files.length === 0) {
		return;
	}
    // display file info
    $('.file-info').text(files[0].name);

    // render preview
    var $preview = $('.image-preview-container'),
        $inner   = $preview.find('.image-preview-container-inner .thumbnail');
    var imgEl = renderImagePreview(files, $preview, $inner);
}

// add selected image to preview
function renderImagePreview(files, $container, $inner) {

    // empty preview
    $inner.empty();

    var file;
    for (var i = 0; i < files.length; i++) {
        file = files[0];
        var imageType = /^image\//;

        if (!imageType.test(file.type)) {
            continue;
        }
        break;
    }

    // 
    // create image element
    var img = document.createElement("img");
        img.classList.add("obj");
        img.file = file;
        img.setAttribute('style', 'max-width: 100%; max-height: 100%;');
    $inner.append($('<div class="image-wrapper" />').append(img)); // Assuming that "preview" is the div output where the content will be displayed.

    // build reader
    var reader = new FileReader();
    reader.onload = (function(_img) {
        return function(ev) { 
            _img.src = ev.target.result; 
        }; 
    })(img);
    reader.readAsDataURL(file);

    return img;
}


//function bindDragNDrop($dropbox) {
//	return $dropbox
//		.on('dragenter', function(ev) {
//			$dropbox.addClass('is-dragging-in');
//				//console.log('dragenter', this, ev);
//			ev.preventDefault();
//			ev.stopPropagation();
//		})
//		.on('dragover', function(ev) {
//				//console.log('dragover');
//			ev.preventDefault();
//			ev.stopPropagation();
//		})
//		.on('dragleave', function(ev) {
//			$dropbox.removeClass('is-dragging-in');
//				//console.log('dragleave', ev);
//			ev.preventDefault();
//			ev.stopPropagation();
//		})
//		.on('drop', function(ev) {
//			ev.preventDefault();
//			ev.stopPropagation();
//			$dropbox.removeClass('is-dragging-in');
//
//            // XXX: this doesn't set the files input
//
//			var dt = ev.originalEvent.dataTransfer;
//			var files = dt.files;
//
//			//
//			handleFiles(files);
//		})
//	;
//}

function bindTypebook($el, defaultData, getSource) {
    const source = getSource(defaultData);

    var minLength = _.isEmpty(defaultData) ? 1 : 0;

	var $typebook = $el.typeahead({
        minLength: minLength,
    }, _.assign({
		name: 'book',
        //source: source,
		source: function (q, sync, async) {
			if (q === '') {
				//sync(source.get('Detroit Lions', 'Green Bay Packers', 'Chicago Bears'));
				sync(defaultData);
			}
			else {
				source.search(q, sync, async);
			}
		},
        sufficient: 10, // 5

        limit: 10,
		display: 'value',
		hint: true,
		templates: {
			notFound: '<div class="empty-message">적당한 책을 찾을 수가 없습니다.</div>',
			pending: '<div class="pending-message">Searching... <i class="glyphicon glyphicon-refresh"></i></div>',
			suggestion: function(context) {
				return `<div target='_blank' id='${context.idStr||""}' class='${context.classStr||""}'>
					<div class='img-wrapper thumbnail'>
						<img class='' src='${context.thumbnail||""}' />
					</div>
					<div class='book-info'>
						<div class='first-row'>
							<span class='book-title'>${context.title}</span>
							<div class='book-subtitle ${context.subtitleStr && context.subtitleStr.length > 0 ? "" : "hide"}' title="${context.subtitleStr}">${context.subtitleStr}</div>
						</div>
						<div class='second-row'>
                            <span class='book-author'>${context.authorsStr||""}</span>
							<span class='book-publisher'>${context.publisher||""}</span>
						</div>
						<div class='third-row'>
							<div class='book-isbn'>${context.isbn}</div>
						</div>
					</div>
					<div class='cleaner'></div>
				</div>`;
            }
		},
	}));


    // deactive focus on window blur
	$(window).on('focus', function(ev) {}).on('blur', function(ev) { 
        $el[0].blur();
    })

    return $typebook;
}


function inputFollowsDrag($dropZone, $clickZone, $inputFile, mouseOverClass) {
    var ooleft    = $dropZone.offset().left;
    var ooright   = $dropZone.outerWidth() + ooleft;
    var ootop     = $dropZone.offset().top;
    var oobottom  = $dropZone.outerHeight() + ootop;

    // $input follows on drag
    $dropZone.on("dragenter", function (ev) {
        ///console.log('dragenter.');
    });
    $dropZone.on("dragover", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        $dropZone.addClass(mouseOverClass);

        var x = ev.pageX;
        var y = ev.pageY;

        var top, left;
        if (ooleft <= x&&x <= ooright && ootop <= y&&y <= oobottom) {
            top  = y - 15;
            left = x - 100;
        } else {
            top  = -400;
            left = -400;
        }
        $inputFile.offset({ top: top, left: left });
    });
    $dropZone.on("dragleave", function (ev) {
        $dropZone.removeClass(mouseOverClass);
    });
    $dropZone.on("drop", function (ev) {
        ///console.log('drop.');
        //ev.preventDefault();
        //ev.stopPropagation();

        $dropZone.removeClass(mouseOverClass);
        $inputFile.offset({top: 0, left: 0}); // reset input position.
    });

    // $input follows inside $clickZone. makes it clickable.
    if ($clickZone && $clickZone.length > 0) {
        var oleft   = $clickZone.offset().left;
        var oright  = $clickZone.outerWidth() + oleft;
        var otop    = $clickZone.offset().top;
        var obottom = $clickZone.outerHeight() + otop;

        $clickZone.mousemove(function (e) {
            var x = e.pageX;
            var y = e.pageY;
            if (!(x < oleft || x > oright || y < otop || y > obottom)) {
                $inputFile.offset({ top: y - 15, left: x - 160 });
            } else {
                $inputFile.offset({ top: -400, left: -400 });
            }
        });
    }

    return $dropZone;
}


//
// initialize
//
function initializeQuoteNew({
    //
    $droppable,
    $clickZone,
    $inputFile,
    $previewInner,
    //
    $bookInput,
    $bookFormGroup
}, recentBooks, typeBookSource) {

    //
	// initialize files input DnD
    //

    // directly set dragover and drop
    //bindDragNDrop($droppable);

    $inputFile = $inputFile.css({
        'position': 'absolute',
        'opacity': 0, // 0,
        //'width': '0.1px',
        //'height': '0.1px',
        //'overflow': 'hidden',
        //'z-index': '-1', // XXX: cannot drop
    }).appendTo($previewInner);

    inputFollowsDrag($droppable, $clickZone, $inputFile, 'is-dragging-in');


    //
	// initialize book type
    //

    // filter recent books
    recentBooks = _.reject(recentBooks, (book) => _.isEmpty(book.raw_response)); // ignore legacy data
    recentBooks = _.map(recentBooks, (book) => {
        return {
            idStr: book.id,
            title: book.title,
            subtitle: '',
            isbn: book.isbn13,
            thumbnail: book.cover_url,
            publisher: '',
            authorStr: '',
            //
            value: book.title,
            raw: book.raw_response||'',
        }
    });

    var $typebook = bindTypebook($bookInput, recentBooks, typeBookSource).on('typeahead:select', function(ev, bookObj) {
        //console.log('selected:', bookObj);
        $bookFormGroup
            .find('input[name="book-isbn"]'     ).val(bookObj.isbn               ).end()
            .find('input[name="book-authors"]'  ).val(bookObj.authorsStr         ).end()
            .find('input[name="book-cover-url"]').val(bookObj.thumbnail          ).end()
            .find('input[name="book-response"]' ).val(JSON.stringify(bookObj.raw)).end()
        ;
    });
}

