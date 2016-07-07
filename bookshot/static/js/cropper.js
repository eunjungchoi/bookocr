(function (name, definition) { // UMD
    if (typeof define === 'function') { // AMD
        define(definition);
    } else if (typeof module !== 'undefined' && module.exports) { // Node.js
        module.exports = definition();
    } else { // Browser
        var theModule = definition(), 
            global    = this, 
            old       = global[name];
        theModule.noConflict = function () {
            global[name] = old;
            return theModule;
        };
        global[name] = theModule;
    }
})('Cropper', function () {

    /* 
     * Cropper 
     *
     * methods:
     *   init
     *   destroy
     *   reset
     *   select
     *   cropImage
     *   $holder
     *
     * events:
     *   initialized
     *   crop
     *   change
     *   select:start
     *   select
     *   release
     *   dblclick
     *
     */
    function Cropper() {
        var c = this;
        c.__jcrop = undefined;
        c._values = {
              fullImageW: undefined, fullImageH: undefined,
              //
              currentSelectionX: 0,         currentSelectionY: 0,
              currentSelectionW: undefined, currentSelectionH: undefined,
              //
              cropImageX: 0,         cropImageY: 0,
              cropImageW: undefined, cropImageH: undefined,
          };
        c._channel = {};

        var _initialized = false;

        /*
         * Create jcrop and display selection
         *
         */
        c.init = function($el, selectRect, _croppedPos, _fullSize) {
            //
            var croppedPos = _croppedPos || {x: 0, y: 0};
            var cropX = c._values.cropImageX = croppedPos.x || 0,
                cropY = c._values.cropImageY = croppedPos.y || 0;

            //
            var fullSize = _fullSize || {};
            if (fullSize.w !== undefined) { c._values.fullImageW = fullSize.w; }
            if (fullSize.h !== undefined) { c._values.fullImageH = fullSize.h; }

            // jcrop
            var isChanging = false;
            $el.Jcrop({
                //baseClass: 'webcrop-jcrop',
                allowMove: false,
                allowReselect: true,
                onChange: function(coord) {

                    var x = coord.x + c._values.cropImageX,
                        y = coord.y + c._values.cropImageY,
                        w = coord.w, 
                        h = coord.h

                    //
                    c._values.currentSelectionX = x;
                    c._values.currentSelectionY = y;
                    c._values.currentSelectionW = w;
                    c._values.currentSelectionH = h;

                    if (!isChanging) {
                        $(c._channel).trigger('select:start', [x,y,w,h]);
                    }
                    isChanging = true;

                    // bind: crop tracker => input
                    $(c._channel).trigger('change', [x,y,w,h]);

                },
                onSelect: function(coord) {
                    isChanging = false;
                    
                    var x = coord.x + c._values.cropImageX,
                        y = coord.y + c._values.cropImageY,
                        w = coord.w, 
                        h = coord.h

                    //
                    c._values.currentSelectionX = x;
                    c._values.currentSelectionY = y;
                    c._values.currentSelectionW = w;
                    c._values.currentSelectionH = h;

                    // bind: crop tracker => input
                    $(c._channel).trigger('select', [x,y,w,h]);
                },
                onRelease: function(coord) {
                    $(c._channel).trigger('release');
                }
            }, function() {
                // save jcrop variable
                var jcrop = c.__jcrop = this;

                // style
                jcrop.ui.holder.css({ 'margin-left' : 'auto', 'margin-right': 'auto' });

                //// bind: tracker click cancels selection
                //var $tracker = jcrop.ui.holder.find("> div > div .jcrop-tracker");
                //var mouseDownPos = undefined;
                //$tracker.mousedown(function(e)  { mouseDownPos = e;         });
                //$tracker.mouseup(function(e)    { mouseDownPos = undefined; });
                //$tracker.mouseleave(function(e) { mouseDownPos = undefined; });
                //$tracker.mousemove(function(e) {
                //    if (mouseDownPos) {
                //        var dist2 = (e.pageX - mouseDownPos.pageX) * (e.pageX - mouseDownPos.pageX) + (e.pageY - mouseDownPos.pageY) * (e.pageY - mouseDownPos.pageY);
                //        if (dist2 > 300) {
                //            jcrop.release();
                //            jcrop.setStartDragMode(mouseDownPos);
                //        } 
                //    } 
                //});

                // select
                c.select(selectRect, {x: cropX, y: cropY});

                // trigger events
                jcrop.ui.holder.find("div .jcrop-tracker").off('dblclick').on('dblclick', function(eventObj) {
                    $(c._channel).trigger('dblclick', eventObj);
                });

                $(c._channel).trigger('initialized', jcrop);
                _initialized = true;
            });
        };

        c.destroy = function() {
            var $img = c.__jcrop.ui.holder.children().last();
            $img.insertAfter(c.__jcrop.ui.holder);
            c.__jcrop.destroy();
        };

        c.reset = function() {
          // crop to null
          var resetRect = {
              x: 0, 
              y: 0,
              w: c._values.fullImageW,
              h: c._values.fullImageH,
          };
          c.cropImage(resetRect);

          // 
          c.select();
        };

        /*
         * select crop tracker
         *
         */
        c.select = function updateCroppingAreaRect(selectRect, croppedPos) {
            if (typeof c.__jcrop === "undefined") {
                return;
            }

            //
            if (selectRect == null) { // null or undefined
                selectRect = {
                    x: 0,
                    y: 0,
                    w: c._values.fullImageW,
                    h: c._values.fullImageH,
                };
            }
            if (selectRect.x === undefined) { return }
            if (selectRect.y === undefined) { return }
            if (selectRect.w === undefined) { return }
            if (selectRect.h === undefined) { return }
            selectRect.x = parseInt(selectRect.x);
            selectRect.y = parseInt(selectRect.y);
            selectRect.w = parseInt(selectRect.w);
            selectRect.h = parseInt(selectRect.h);

            // use current cropped x and y value
            croppedPos = croppedPos || {};
            var croppedX = croppedPos.x, 
                croppedY = croppedPos.y;
            if (croppedX === undefined) { croppedX = c._values.cropImageX }
            if (croppedY === undefined) { croppedY = c._values.cropImageY }

            //
            var selectStartX = selectRect.x - croppedX,
                selectStartY = selectRect.y - croppedY;

            c.__jcrop.setSelect([
                selectStartX,          
                selectStartY,
                selectStartX + selectRect.w, 
                selectStartY + selectRect.h
            ]);
        };
      
        /*
         * function updateCroppedImageSize(rect)
         *
         * crop image to given rect (client-side)
         */
        c.cropImage = function updateCroppedImageSize(cropRect) {

            //
            cropRect = cropRect || {};
            cropRect.x = typeof cropRect.x === 'undefined' ? c._values.currentSelectionX : cropRect.x;
            cropRect.y = typeof cropRect.y === 'undefined' ? c._values.currentSelectionY : cropRect.y;
            cropRect.w = cropRect.w || c._values.currentSelectionW;
            cropRect.h = cropRect.h || c._values.currentSelectionH;

            // temporarily disable jcrop
            var $img = c.__jcrop.ui.holder.children().last();
            $img.insertAfter(c.__jcrop.ui.holder);
            c.__jcrop.destroy();

            // update css background to current selected area
            //console.log('[cropRect]', cropRect);
            $img.css({
                'width':  cropRect.w,
                'height': cropRect.h,
                "background-position-x": "-" + (cropRect.x) + "px",
                "background-position-y": "-" + (cropRect.y) + "px"
            });

            // re-enable jcrop
            c.init($img, cropRect, {x:cropRect.x, y:cropRect.y});

            // set data
            c._values.cropImageX = cropRect.x;
            c._values.cropImageY = cropRect.y;
            c._values.cropImageW = cropRect.w;
            c._values.cropImageH = cropRect.h;

            // trigger
            $(c._channel).trigger('crop', cropRect);
        };

        c.$holder = function() {
            return c.__jcrop.ui.holder;
        };
        c.$selection = function() {
            return c.__jcrop.ui.selection;
        };

        // bind/unbind events
        c.on = function(_arguments) {
            if (arguments[0] === 'initialized' && _initialized) {
                var callback = arguments[arguments.length - 1];
                callback();
                return;
            }

            var self = $(c._channel);
            self.on.apply(self, arguments);
        };
        c.once    = function(_arguments) { bindToChannel($(c._channel), "one", arguments); };
        c.off     = function(_arguments) { bindToChannel($(c._channel), "off", arguments); };
        c.trigger = function(_arguments) { bindToChannel($(c._channel), "trigger", arguments); };
        function bindToChannel(self, methodName, args) {
            self[methodName].apply(self, args);
        }
    }

    return Cropper;
});

