$( document ).ready(function() {
    // Your code here
});

var pathname = window.location.pathname;

function show_activity() {
    //$("#activity").show().animate({opacity: 1.0}, 3000).fadeOut(1000);
    $("#activity").show();
}

function set_sort_order() {
    order = $("#sort_order").val();
    show_activity();
    $.ajax({ url: "/reorder" + pathname,
                     data: {csrfmiddlewaretoken: document.getElementsByName('csrf_token')[0].value,
                            sort_order: order,
                            },
                     type: 'POST',
                     success: function(data) {
                        $("#images").html(data);
                        $("#activity").fadeOut("fast");
                     },
    });
}

function set_sort_by() {
    order = $("#sort_by").val();
    show_activity();
    $.ajax({ url: "/reorder" + pathname,
                     data: {csrfmiddlewaretoken: document.getElementsByName('csrf_token')[0].value,
                            sort_by: order,
                            },
                     type: 'POST',
                     success: function(data) {
                        $("#images").html(data);
                        $("#activity").fadeOut("fast");
                     },
    });
}

function set_num_per_page() {
    num = $("#num_per_page").val();
    $.ajax({ url: "/reorder/",
                     data: {csrfmiddlewaretoken: document.getElementsByName('csrf_token')[0].value,
                            num_per_page: num,
                            },
                     type: 'POST',
                     success: function(data) {
                         window.location = "/";
                     },
    
    });

}


