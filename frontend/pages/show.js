/*
** JavaScript for Powerwiki show
*/

$('document').ready(function () {
  // Detect DOM elements
  var $window = $(window),
    $edit = $('a#powerwiki_edit')
    ;

  // Save shortcut
  $(window).keypress(function (e) {
    if (!(e.which == 101 && e.ctrlKey) && !(e.which == 19)) {
      return true;
    }
    e.preventDefault();
    document.location = $edit.attr('href');
    return false;
  });
});

