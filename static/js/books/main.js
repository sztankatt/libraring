/*BOOKS */
function load_all_books(section, output){
    $.ajax({
        type:'POST',
        dataType: 'html',
        data: {'section': section, 'csrfmiddlewaretoken':$.cookie('csrftoken')},
        url: '/ajax/load/all/books/',
        success: function(data){
            output(data);
        }
    })
}

function load_books(load_type){
        //check if type is defined. if not, load the tab which is active.
        var type = (load_type == undefined) ? $('#book_list_nav li.active a').attr('data-load') : load_type;

        var active_tab = $('a[data-load="'+type+'"]').attr('href');

        
        $(active_tab+' .book-list').load('/ajax/list/books/', {'type':type, 'csrfmiddlewaretoken': $.cookie('csrftoken')}, function(){
            var $container = $('.book-page-row .book-list');
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
            
           $('a.load-more-books').click(function(event){
                event.preventDefault();
                $this = $(this);
                load_all_books($this.attr('data-section'), function(data) {
                    $this.parent().before(data);

                    $container.imagesLoaded(function(){
                        $container.masonry('reloadItems');
                        $container.masonry();
                    });

                    $this.parent().remove();
                });
            });
            
        });
}

$(document).ready(function(){    
    $('#book_list_nav li a').click(function(){
       // var href = $(this).attr('href');
        //var html = $(href+' .book-list').html() ;

//        console.log(html);

  //      if (html == "") {
            var type = $(this).attr('data-load');
            load_books(type);
    //    }
    });
    
    load_books();
    



    //search results
    (function(){
        var $container = $('#search_results .book-list');
        
        $container.masonry({
            gutter: '.book-gutter-sizer',
            columnWidth: '.book-grid-sizer',
            itemSelector: '.book-container',
        });
    
        
        $container.imagesLoaded(function(){
            $container.masonry();
        });
    })();


    // make new publisher field disable when we select an existing one
    $('#id_publisher').change(function(){
        if ($(this).val() != ""){
            $('#id_new_publisher').attr({'disabled':'true'})
        }
        else{
            $('#id_new_publisher').attr({'disabled':'false'})
        }
    });
    

});