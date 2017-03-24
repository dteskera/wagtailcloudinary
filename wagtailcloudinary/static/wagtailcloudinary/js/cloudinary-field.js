(function($){
  'use strict';
  $(document).ready(function() {
    $('.js-wagtailcloudinary').on('click', function(e){
      e.preventDefault();
      var link = $(this);
      var id = link.data('target')
      ModalWorkflow({
        url: link.data('url'),
        responses: {
          imageChosen: function(imageData) {
            var preview_id = '#preview_' + id;
            var input = $('#'+id);
            var preview = $('#preview_' + id);

            input.val(imageData.value);
            var chooser = link.closest('.image-chooser');
            if (imageData.url != ''){
              preview.attr({src: imageData.url})
              chooser.removeClass('blank');
            } else {
              chooser.addClass('blank');
              preview.attr({src: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw'})
            }
          }
        }
      });
    });
    $('.js-wagtailcloudinary-clear').on('click', function(e){
      e.preventDefault();
      var link = $(this);
      link.closest('.image-chooser').addClass('blank');
      $('#'+link.data('target')).val('');
      $('#preview_'+link.data('target')).attr('src', 'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw');
    });
  });
})(jQuery);
