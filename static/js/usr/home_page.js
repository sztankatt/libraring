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

    function increaseLoadUntil(){
        hash = History.getState().hash;
        len = hash.length;
        if(hash.indexOf("?")>-1){
            index = hash.indexOf("page-number");
            if(index > -1){
                parts = hash.split("page-number=");
                vars = parts[1].split("&");
                next_page = vars[0]*1;
                next_page = next_page + 1;
                vars.splice(0, 1);
                url = parts[0]+"page-number="+next_page+vars.join('');
                History.replaceState(null, null, url);
            }
            else{
                History.replaceState(null, null, hash+"&page-number=2");
            }
        }
        else{
            History.replaceState(null, null, "?page-number=2");
        }
    }

    $.endlessPaginate({
        paginateOnScroll: true,
        onCompleted: function(context, fragment) {
            increaseLoadUntil();
            num = context.url.split("page=")[1];
            $items = $('.page-num-'+num+' .book-grid-sizer');
            msnry = $('#genre_books_all').data('masonry');
            imagesLoaded($items, function(){
                msnry.appended($items);
            });
        }
    });

    $('.main-menu-navbar .toggle-collapse-menu').click(function(){
        $('ul.main-menu-left').slideToggle('fast');
    });

    $(window).resize(function(){
        if(window.innerWidth > 500){
            $('ul.main-menu-left').show();
        }
        else{
            $('ul.main-menu-left').hide();
        }
    });



});