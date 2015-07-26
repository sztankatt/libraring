function add_to_watchlist(book_id, change) {
    $.ajax({
        'type':'GET',
        'dataType':'json',
        'url' : '/ajax/add/to/watchlist/',
        'data': {'book_id':book_id, 'change':change},
        'success' :function(data){
            $button = $('.watchlist');
            if (data.watchlist) {
                $button.addClass('active');
                $button.children('span.glyphicon').removeClass('glyphicon-plus').addClass('glyphicon-ok');
                $button.children('span.watchlist-text').html('Added to watchlist');
            }
            else{
                $button.removeClass('active');
                $button.children('span.glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-plus');
                $button.children('span.watchlist-text').html('Add to watchlist');
            }
        }
    });
}

$(document).ready(function(){

	 add_to_watchlist($('.watchlist').val(), "false");
    
    $('.watchlist').click(function(){ add_to_watchlist($(this).val(), "true"); });

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
            }, 500);
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
            }, 500);
            $(".left-side .left-nav-body").fadeIn("fast");
            $this.children('.text').fadeIn("fast");
        }

    });
   
});