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
   
});