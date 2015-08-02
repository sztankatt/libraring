$(document).ready(function(){

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
});