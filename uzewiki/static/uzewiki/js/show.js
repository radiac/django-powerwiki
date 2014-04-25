/*
** JavaScript for Uzewiki show
*/

$('document').ready(function () {
    // Detect DOM elements
    var $window = $(window),
        $edit = $('a#uzewiki_edit')
    ;
    
    // Save shortcut
    $(window).keypress(function(e) {
        if (!(e.which == 101 && e.ctrlKey) && !(e.which == 19)) {
            return true;
        }
        e.preventDefault();
        document.location = $edit.attr('href');
        return false;
    });
});

