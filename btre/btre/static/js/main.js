const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

$(document).on('click', '[data-toggle="lightbox"]', function(event) 
{ event.preventDefault();
    $(this).ekkoLightbox();
});

setTimeout(function() {
    $('#message').fadeOut('slow');

},3000)