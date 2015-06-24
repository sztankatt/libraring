$(document).ready(function(){

	$('.genre-books-container').each(function(){
		$container = $(this);

		$container.masonry({
            gutter: '.book-gutter-sizer',

            columnWidth: '.book-grid-sizer',
            itemSelector: '.book-container',
        });
    
        
        $container.imagesLoaded(function(){
            $container.masonry();
        });


	});
});