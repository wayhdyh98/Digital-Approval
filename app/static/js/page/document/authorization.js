var check_pemohon
$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    initialize_component();

    // data grid
    initialize_data();
    console.log(check_pemohon)

    $.LoadingOverlay("hide");
});



function pictype_onchange(value) {
    // pemohon
    if (value == "0") {
        $("#master-pic-select").hide(100);
        $("#free-text-select").show(100);
    }
    else {
        $("#master-pic-select").show(100);
        $("#free-text-select").hide(100);
        
        $("#authorization-picapproval-select").val(0);
        approvaltype_onchange(0);
        prepare_approval("authorization-picid-select", $("#authorization-picdivision-select").val());
    }
}

function approvaltype_onchange(value) {
    if (value == "0") {
        $("#division-pic-select").hide(100);
        $("#free-text-select").show(100);
    }
    else {
        $("#division-pic-select").show(100);
        $("#free-text-select").hide(100);
    }
}

// select approval type
$('#authorization-picapproval-select').on('change', function() {
    approvaltype_onchange(this.value);
});


$('#authorization-pictype-select').on('change', function() {
    pictype_onchange(this.value);
});


function prepare_parentlevel(container) {
    var url = url_pic_parentapproval + "/" + $("#documentid-text").val();
    var params = null;

    function success_callback(data) {
        $('#' + container).children().remove().end();
        data.data.forEach(element => {
            picname = (element.picname == null ? "Choosen later" : element.picname)
            pictype = (element.pictype == "0" ? "Pemohon" : (element.pictype == "1" ? "Mengetahui" : "Menyetujui"))
            $("#" + container).append(`<option value="${element.piclevel}">${element.piclevel}. ${pictype} - ${picname}</option>'`);
        });
    }

    function error_callback() {
    }

    page.read_data(url, params, 'GET', success_callback, error_callback);
}


function initialize_component() {
    $("#master-pic-select").hide(100);
    $("#free-text-select").show(100);

    $("#authorization-description-text").val("");

    prepare_division("authorization-picdivision-select");
    prepare_parentlevel("authorization-pic-parentlevel-select");

    // select divison on change
    $('#authorization-picdivision-select').on('change', function() {
        prepare_approval("authorization-picid-select", this.value);
    });
}


function initialize_data() {
    var url = url_master_approvals + "/" + $("#documentid-text").val();

    function success_callback(data) {
        check_pemohon = data.checkpemohon
        $.grid_main("grid-main", data.data, "masterapproveid", browse_column());
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}


function delete_approval(approveid) {
    var url = url_delete_approval;
    var params = {
        "approveid": approveid
    }

    function success_callback(data) {
        if (data.success == '1') {
            Swal.fire('Delete!', '', 'success').then(function () {
                initialize_data();
            });
        }
    }

    function error_callback() {
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
}


/* define the column of the grid  */
browse_column = function () {
    return [
        {
            allowExporting: false,
            caption: "#",
            width: 100,
            fixed: true,
            headerCellTemplate: function (header, info) {
                $('<a>New</a>')
                    .attr('href', '#')
                    .click(function () {
                        $("#authorization-description-text").val("");
                        $("#authorization-pictype-select").val(0);
                        $("#master-pic-select").hide(100);
                        $("#free-text-select").show(100);
                        $("#authorization-mandatory-check").prop("checked", false);
                        prepare_parentlevel("authorization-pic-parentlevel-select");
                        $("#authorization-modal").modal('show');
                    })
                    .appendTo(header);
            },
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                $('<a class="btn btn-sm btn-danger col"><i class="fa fa-trash" aria-hidden="true"></i> Delete</a>')
                    .attr('href', '#')
                    .click(function () {
                        Swal.fire({
                            title: 'Do you want to delete the data?',
                            showDenyButton: true,
                            showCancelButton: true,
                            confirmButtonText: 'Delete',
                            denyButtonText: `Don't delete`,
                        }).then((result) => {
                            /* Read more about isConfirmed, isDenied below */
                            if (result.isConfirmed) {
                                delete_approval(info.data.masterapproveid);
                            } else if (result.isDenied) {
                                Swal.fire('Data are not deleted', '', 'info')
                            }
                        })
                    }
                    )
                    .appendTo($el);

                container.append($el);
            },
        },
        {
            dataField: "pictype",
            caption: "Type",
            visible: false,
        },
        {
            dataField: "pictypetext",
            caption: "Type",
            alignment: 'center',
        },
        {
            dataField: "piclevel",
            caption: "PIC Level",
            alignment: 'center',
        },
        {
            dataField: "picsublevel",
            caption: "PIC Sub Level",
            alignment: 'center',
        },
        {
            dataField: "picid",
            caption: "PIC ID"
        },
        {
            dataField: "picname",
            caption: "PIC Name"
        },
        {
            dataField: "description",
            caption: "Approval Sign Title"
        },
        {
            dataField: "mandatory",
            caption: "Is Mandatory?",
            visible: false,
        },
        {
            dataField: "mandatorytext",
            caption: "Is Mandatory?",
            alignment: 'center',
            cellTemplate: function (container, options) {
                if (options.value == "Mandatory") {
                    $('<h6><span class="badge badge-success col">Mandatory</span></h6>').appendTo(container);
                }
                else {
                    $('<h6><span class="badge badge-danger col">Not Mandatory</span></h6>').appendTo(container);
                }
            },
        },
    ];
}

$("#authorization-mandatory-check").change(() => {
    if ($("#authorization-mandatory-check").is(':checked')) {
        $('#authorization-sublevel-check').attr("disabled", true)
        $("#authorization-pic-parentlevel-select").attr("disabled", true)
    } else {
        $('#authorization-sublevel-check').attr("disabled", false)
        $("#authorization-pic-parentlevel-select").attr("disabled", false)
    }
})

$("#authorization-sublevel-check").change(() => {
    if ($("#authorization-sublevel-check").is(':checked')) {
        $('#authorization-mandatory-check').attr("disabled", true)
    } else {
        $('#authorization-mandatory-check').attr("disabled", false)
    }
})

$(document).on("click", ".btn-save", function () {
    var url = url_insert_approval;

    var picid = $("#authorization-picid-select").val();
    if ($("#authorization-pictype-select").val() == "0") {
        picid = "";
    }
    if ($("#authorization-picapproval-select").val() == "0") {
        picid = "";
    }

    // check for mandatory
    var mandatory_check = "0";
    if ($('#authorization-mandatory-check').is(":checked"))
    {
        mandatory_check = "1";
    }

    // check for sublevel
    var sublevel_check = "0";
    if ($('#authorization-sublevel-check').is(":checked"))
    {
        sublevel_check = "1";
    }
    var piclevel = 0;
    if (sublevel_check == "1") {
        piclevel = $("#authorization-pic-parentlevel-select").val();
    }

    var params = {
        "documentid": $("#documentid-text").val(),
        "picid": picid,
        "piclevel": piclevel,
        "pictype": $("#authorization-pictype-select").val(),
        "mandatory": mandatory_check,
        "description": $("#authorization-description-text").val()
    }

    if ($("#authorization-picapproval-select").val() == "1" && picid == "0") {
        Swal.fire({
            title: `Please pick the approval name!`,
            icon: 'error'
        })
    } else if (check_pemohon == "true" && $("#authorization-pictype-select").val() == 0) {
        Swal.fire({
            title: `Pemohon can't be multiple!`,
            icon: 'error'
        })
    } else if (piclevel == 1 && $("#authorization-pictype-select").val() != 0) {
        Swal.fire({
            title: `Level 1 only be aquired by Pemohon Type!`,
            icon: 'error'
        })
    }  else {
        $.LoadingOverlay("show");
        function success_callback(data) {
            if (data.success == "1") {
                initialize_data();
                $('#authorization-sublevel-check').attr("disabled", false)
                $("#authorization-sublevel-check").prop("checked", false)
                $("#authorization-pic-parentlevel-select").attr("disabled", false)
                $('#authorization-mandatory-check').attr("disabled", false)
                $("#authorization-mandatory-check").prop("checked", false)
                $("#authorization-modal").modal('hide');
            }
            $.LoadingOverlay("hide");
        }

        function error_callback() {
            $.LoadingOverlay("hide");
        }

        page.read_data(url, params, 'POST', success_callback, error_callback);
    }

});