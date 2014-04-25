/*
** JavaScript for Uzewiki edit
*/

$('document').ready(function () {
    // Detect DOM elements
    var $window = $(window),
        $container = $('body'),
        $content = $('#id_content'),
        $form = $('form.wiki_form')
    ;
    
    // Don't want the edit window to get too small
    var MIN_HEIGHT = 200;
    
    // Expand the content to max the body
    var maxHeightTimeout = null;
    function maxHeight() {
        $content.height(10);
        clearTimeout(maxHeightTimeout);
        maxHeightTimeout = setTimeout(function () {
            $content.height(Math.max(
                MIN_HEIGHT, $window.height() - ($container.height() - 10)
            ));
        }, 100);
    }
    maxHeight();
    $window.resize(function () {
        maxHeightTimeout = setTimeout(maxHeight, 250);
    });
    
    // Save shortcut
    $window.keypress(function(e) {
        if (!(e.which == 115 && e.ctrlKey) && !(e.which == 19)) {
            return true;
        }
        e.preventDefault();
        $form.submit();
        return false;
    });
});

