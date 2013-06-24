$( document ).ready(function() {
    // Your code here
    document.onkeydown = function(e) {
            e = e || window.event; // because of Internet Explorer quirks...
            k = e.which || e.charCode || e.keyCode; // because of browser differences...

            if (k == 72 && !e.altKey && !e.ctrlKey && !e.shiftKey) {
                target = $("#prev").attr('href');
                if (target != undefined) {
                    window.location = target;
                }
            } else if (k == 76 && !e.altKey && !e.ctrlKey && !e.shiftKey) {
                target = $("#next").attr('href');
                if (target != undefined) {
                    window.location = target;
                }
            } else if (k == 74 && !e.altKey && !e.ctrlKey && !e.shiftKey) {
                window.location = $("#random").attr('href');
            } else if (k == 75 && !e.altKey && !e.ctrlKey && !e.shiftKey) {
                window.location = $("#back").attr('href');
            } else {
                return true; // it's not a key we recognize, move on...
            }
            return false; // we processed the event, stop now.
    }
});


