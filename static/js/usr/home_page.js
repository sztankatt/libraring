$(document).ready(function(){

		
	var $container = $('#genre_books_all');
    
    $container.masonry();
    $container.masonry('destroy');
    
    $container.masonry({
        gutter: '.book-gutter-sizer',

        columnWidth: '.book-grid-sizer',
        itemSelector: '.book-container',
    });
    
    $container.imagesLoaded(function(){
        $container.masonry();
    });
            

});