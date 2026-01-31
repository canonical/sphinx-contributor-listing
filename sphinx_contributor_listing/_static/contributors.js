$(document).ready(function() {
    $(document).on("click", function () {
        $(".all-contributors").hide();
        $("#all-contributors-overlay").hide();
    });

    $('.display-contributors').click(function(event) {
        $('.all-contributors').toggle();
        $("#all-contributors-overlay").toggle();
        event.stopPropagation();
    });
})
