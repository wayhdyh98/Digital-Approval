$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    prepare_form();
    $('#select-document-type').change()

    $.LoadingOverlay("hide");
});


// division 
function prepare_division() {
    var url = url_master_divisions;
    var params = null;

    function success_callback(data) {
        data.data.forEach(element => {
            $("#select-division-id").append('<option value='+ element.divisionid +'>'+ element.divisionname +'</option>');
        });
        $("#select-division-id").find( 'option:first' ).prop('selected',true).change()
    }

    function error_callback() {
    }

    page.read_data(url, params, 'GET', success_callback, error_callback);

    // select on change
    $('#select-division-id').on('change', function() {
        prepare_document(this.value);
    });
}


$('#select-document-type').on('change', function() {
    $("#select-document-text").val($("#select-document-type option:selected").text())
    $("#select-designdocument-version").val($("#select-document-type option:selected").attr('data-activeversion'))
});


// document
function prepare_document(divisionid) {
    var url = url_request_document + "/" + divisionid
    var params = null;

    function success_callback(data) {
        $('#select-document-type').children().remove().end();
        data.data.forEach(element => {
            $("#select-document-type").append(`<option value="${element.masterdocid}" data-activeversion="${element.activeversiondocument}">${element.name} (v${element.version.charAt(0)}.${element.activeversiondocument})</option>`);
        });
        $('#select-document-type').find( 'option:first' ).prop('selected',true).change()
    }

    function error_callback() {
    }

    page.read_data(url, params, 'GET', success_callback, error_callback);
}


function prepare_form() {
    prepare_division();
}

$(document).on("click", ".btn-next", function () {
    $("form").submit(function(e){
        if ($('#select-document-type').val() != null && $('#select-document-type').find(':selected').data('activeversion') != null) {
            $('form').submit()
        } else if ($('#select-document-type').val() == null) {
            e.preventDefault();
            Swal.fire(
                "Document Type can't be empty!",
                'Please fill the Document Type',
                'error'
            )
        } else if ($('#select-document-type').find(':selected').data('activeversion') == null) {
            e.preventDefault();
            Swal.fire(
                "Design Document is not found!",
                'Please create Design Document first',
                'error'
            )
        }
    });
});