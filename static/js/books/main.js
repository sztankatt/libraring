/*BOOKS */
$(document).ready(function(){
   var $container = $('#search_results div.book-list');

    $container.masonry();
    $container.masonry('destroy');

    $container.masonry({
        gutter: '.book-gutter-sizer',

        columnWidth: '.book-grid-sizer',
        itemSelector: '.book-container'
    });

    $container.imagesLoaded(function(){
        $container.masonry();
    });
});