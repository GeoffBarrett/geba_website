function customFilePicker(cb, value, meta) {
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');

    /*
      Note: In modern browsers input[type="file"] is functional without
      even adding it to the DOM, but that might not be the case in some older
      or quirky browsers like IE, so you might want to add it to the DOM
      just in case, and visually hide it. And do not forget do remove it
      once you do not need it anymore.
    */

    input.onchange = function () {
        var file = this.files[0];
        var reader = new FileReader();
        onImageUpload(file);
    }

    function onImageUpload ( files ) {
        // custom attachment data
        var attachmentData = origin.dataset;
        $nImageInput.fileupload();
        var jqXHR = $nImageInput.fileupload('send',
            {
                files: files,
                formData: $.extend({csrfmiddlewaretoken: csrftoken}, attachmentData),
                url: settings.url.upload_attachment,
            })
            .done(function (data, textStatus, jqXHR) {
                $.each(data.files, function (index, file) {
                    $sn.summernote("insertImage", file.url);
                });
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                // if the error message from the server has any text in it, show it
                var msg = jqXHR.responseText;
                if (msg.length > 0) {
                    alert('Got an error uploading an image: ' + msg);
                }
                // otherwise, show something generic
                else {
                    alert('Got an error while uploading images.');
                }
            });
    }

    input.click();

}


function customFilePicker2(callback, value, meta) {
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');

    if (meta.filetype == 'image') {
        //var input = document.getElementById('my-file');

        input.click();
        input.onchange = function () {
            var file = input.files[0];

        };
    }
}

