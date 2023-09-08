var arrayfile = []
var uuidkomp = ''
var arrayuuid = []
$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    $('#filequestion').change()
    check_answer()

    $.LoadingOverlay("hide");
});

$('#filequestion').change(function() {
    if(this.checked) {
        $("#yes-text").css("color", "#e8647c")
        $("#no-text").css("color", "#6c757d")
        $(".div-upload").show()
        $("#filequestion").val("1")

        if ($(".upload-file").length == 0) {
            $(".btn-add").click()
        }
    } else {
        $("#no-text").css("color", "#e8647c")
        $("#yes-text").css("color", "#6c757d")
        $(".div-upload").hide()
        $("#filequestion").val("0")
    }       
});

function check_answer() {
    var url = url_answer_submissions_filerequest + "/" + $("#requestapprovalid").val()

    function success_callback(data) {
        if (data.data.length > 0) {
            $('#filequestion').prop('checked', true).change()
            
            data.data.forEach(element => {
                arrayuuid.push({ 
                    "uuid": uuidkomp,
                    "fileid": element.approvalonlinefileid,
                    "filename": element.filename,
                    "size": element.size
                })

                if ($(".upload-file").length < data.data.length) {
                    $(".btn-add").click()
                }
            })

            arrayuuid.forEach(element => {
                replace_component(element.uuid, element.fileid, element.filename, element.size, 0)
            })
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$(document).on("click", ".btn-add", function () {
    uuidkomp = uuidv4()
    $(".upload-area")
    .append($(`<div class="mb-3" data-component="${uuidkomp}" data-parent="${uuidkomp}">`)
    .append($(`<div data-component-area="${uuidkomp}">`)
    .append(`<label for="uploadlampiran" class="form-label">Please Upload Your Attachment File</label>`)
    .append($('<div class="input-group">').append(`<input class="form-control upload-file" data-component="${uuidkomp}" name="upload-${uuidkomp}" type="file">`))));
});

$(document).on("click", ".btn-del", function () {
    var url = url_delete_request_files;
    var uuid = $(this).context.attributes["data-component"].value
    var fileid = $(this).context.attributes["data-fileid"].value

    params = {
        "approvalonlinefileid": fileid
    }
    
    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.success == "1") {
            replace_component(uuid, "", "", "", 1)
        }
        $.LoadingOverlay("hide");
    }
    function error_callback() {
        $.LoadingOverlay("hide");
    }
    
    page.read_data(url, params, 'POST', success_callback, error_callback);
});

// upload files
$(document).on("change", ".upload-file", function () {
    var url = url_upload_request_files;
    var uuid = $(this).context.attributes["data-component"].value
    var params = new FormData();
    var files = this.files[0];
    
    params.append('file', files);
    params.append('filename', files.name);
    params.append('requestapprovalid', $("#requestapprovalid").val());

    if (files.size > 510000) {
        Swal.fire("File size is too big!", "Max. 500KB", "error");
        this.files[0].value = "";
        this.value = ""
    } else {
        $.LoadingOverlay("show");
        function success_callback(data) {
            if (data.success == "1") {
                replace_component(uuid, data.result, files.name, files.size, 0);
                $.LoadingOverlay("hide");
            }
            else {
                Swal.fire(data.message, '', 'error');
                $.LoadingOverlay("hide");
            }
            // reset
            $(this).val(null);
        }

        $.ajax({
            url: url,
            type: 'post',
            data: params,
            contentType: false,
            processData: false,
            success: function (response) {
                success_callback(response);
            },
        });
    }
});

function replace_component(uuid, fileid, filename, size, condition) {
    if (condition == 0) {
        $(`[data-component-area="${uuid}"]`).remove()
        $(`[data-parent="${uuid}"]`)
        .append($(`<div data-component-area="${uuid}">`)
        .append($('<div class="input-group">').append(`<button type="button" class="btn btn-danger btn-del mr-2" data-component="${uuid}" data-fileid="${fileid}"><i class="fa-solid fa-trash"></i></button>`).append(`<a href="${url_download_request_files}/${fileid}" for="uploadlampiran" class="form-label mr-2" target="blank">${filename}</a>`).append(`<small class="text-danger font-italic" data-component="${uuid}">(${size}kb)</small>`)));
    } else {
        $(`[data-component-area="${uuid}"]`).remove()
        $(`[data-parent="${uuid}"]`)
        .append($(`<div data-component-area="${uuid}">`)
        .append(`<label for="uploadlampiran" class="form-label">Please Upload Your Attachment File</label>`)
        .append($('<div class="input-group">').append(`<input class="form-control upload-file" data-component="${uuid}" name="upload-${uuid}" type="file">`)));
    }
}

$(document).on("click", ".btn-next", function () {
    checkbox = $("#filequestion").val()
    if (checkbox == "1") {
        if ($(".upload-file").length > 0) {
            Swal.fire('Terdapat file upload yang belum terisi', '', 'error');
        } else {
            window.open(`/submission/submissions/postingrequest/${$("#requestapprovalid").val()}`, '_self')
        }
    } else {
        window.open(`/submission/submissions/postingrequest/${$("#requestapprovalid").val()}`, '_self')
    }
    
});