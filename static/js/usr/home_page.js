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


    $(".left-nav-footer button").click(function(){
        $this = $(this);
        if($this.hasClass('normal')){
            $this.removeClass('normal').addClass('slided');
            $(".left-side .left-nav-body").fadeOut("fast");
            $this.children('.text').fadeOut();

            $this.removeClass('btn-block').animate({
                width:"30px",
                padding:"6px 6px"
            }).children('i').css({'margin':'0px'}).removeClass('fa-minus').addClass('fa-plus');

            $(".home-container .left-side").animate({
                width: "50px"
            }, 500);

            $(".home-container .right-side").animate({
               marginLeft:"50px"
            }, 500, function(){
                $container.masonry();
            });
        }
        else{
            $this.removeClass('slided').addClass('normal');
            $this.addClass('btn-block').animate({
                width:"180px",
                padding:"6px 12px"
            }).children('i').css({'margin':'5px'}).removeClass('fa-plus').addClass('fa-minus');

            $(".home-container .left-side").animate({
                width: "200px"
            }, 500);

            $(".home-container .right-side").animate({
               marginLeft:"200px"
            }, 500, function(){
                $container.masonry();
            });
            $(".left-side .left-nav-body").fadeIn("fast");
            $this.children('.text').fadeIn("fast");
        }

    });



});