var designdocument_groupquestion_id
var sectiontype

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    initialize_document()

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});


function initialize_document() {
    var url = url_master_documents;

    function success_callback(data) {
        $("#from-documentcopy-select").children().remove().end();
        $("#from-documentcopy-select").append(`<option value=0>No</option>`)
        if (data.data.length > 0) {
            data.data.forEach(element => {
                $("#from-documentcopy-select").append(`<option value=${element.masterdocid}>${element.name} (v${element.version})</option>`)
            })
        }
        $("#from-documentcopy-select").find('option:first').prop('selected',true).change()
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$("#from-documentcopy-select").change(function () {
    if ($(this).val() != 0) {
        $(".select-groupsection").show()
        initialize_data("select", $(this).val())
    } else {
        $(".select-groupsection").hide()
    }
})

function initialize_data(condition = "grid", documentid = $("#documentid-text").val()) {
    var url = url_designdocument_groupquestions + "/" + documentid;

    function success_callback(data) {
        if (condition == "grid") {
            $.grid_main("grid-main", data.data, "designdocumentgroupquestionid", browse_column());
        } else {
            $("#from-groupsectioncopy-select").children().remove().end();
            if (data.data.length > 0) {
                data.data.forEach(element => {
                    $("#from-groupsectioncopy-select").append(`<option value=${element.designdocumentgroupquestionid}>${element.grouptitle}</option>`)
                })
            }
            $("#from-groupsectioncopy-select").find('option:first').prop('selected',true).change()
        }
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}


function initialize_data_question(designdocumentgroupquestionid) {
    var url = url_designdocument_questions + "/" + $("#documentid-text").val() + "/" + designdocumentgroupquestionid;

    function success_callback(data) {
        $.grid_main("grid-main-question", data.data, "designdocumentgroupquestionid", browse_column_question());
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function initialize_data_multichoice(designdocumentgroupquestionid) {
    var url = url_designdocument_questions_multichoice + "/" + designdocumentgroupquestionid;

    function success_callback(data) {
        data.data.forEach(element => {
            var data_temp = {
                "questionid": designdocumentgroupquestionid,
                "code": element["code"],
                "value": element["[value]"]
            }
            multichoice.push(data_temp)
            $("#question-multichoice-select").append('<option value=' + data_temp.code + '>' + data_temp.value + '</option>');
            $("#question-multichoice-text").val("");
            $("#question-multichoice-select").val(data_temp.code);
            clone_multichoice();
        })
        
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}


/* define the column of the grid  */
browse_column = function () {
    return [
        {
            caption: "#",
            width: 220,
            fixed: true,
            headerCellTemplate: function (header, info) {
                $('<a>New</a>')
                    .attr('href', '#')
                    .click(function () {
                        $(".select-document").show();
                        $("#groupquestionid-text").val("-1");
                        $("#groupquestion-title-text").val("");
                        $("#groupquestion-modal").modal('show');
                        $("#group-sectiontype-select").find('option:first').prop('selected',true).change()
                    })
                    .appendTo(header);
            },
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                $('<a class="btn btn-sm btn-dark col-md-4"><i class="fa fa-pen" aria-hidden="true"></i> Edit</a>')
                    .attr('href', '#')
                    .click(function () {
                        $(".select-document").hide();
                        $("#groupquestionid-text").val(info.data.designdocumentgroupquestionid);
                        $("#groupquestion-title-text").val(info.data.grouptitle);
                        $("#group-sectiontype-select").val(info.data.sectiontype);
                        $("#groupquestion-modal").modal('show');
                    }
                    )
                    .appendTo($el);
                $('<a class="btn btn-sm btn-danger col-md-4"><i class="fa fa-trash" aria-hidden="true"></i> Delete</a>')
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
                                delete_groupquestion(info.data.designdocumentgroupquestionid);
                            } else if (result.isDenied) {
                                Swal.fire('Data are not deleted', '', 'info')
                            }
                        })
                    }
                    )
                    .appendTo($el);
                $(`<a class="btn btn-sm btn-info col-md-4" id="${info.data.designdocumentgroupquestionid}"><i class="fa fa-eye" aria-hidden="true"></i> Select</a>`)
                    .attr('href', '#')
                    .click(function () {
                        $('html, body').animate({
                            scrollTop: $("#question-section").offset().top
                        }, 50);

                        $('#question-groupquestionid-text').removeData("question-groupquestionid-text");

                        $("#question-section").css("visibility", "visible")
                        $("#question-text").text("Question From Section " + info.data.grouptitle)
                        initialize_data_question(info.data.designdocumentgroupquestionid)

                        $('#question-groupquestionid-text').attr("data-question-groupquestionid-text", info.data.designdocumentgroupquestionid);

                        // Save Group Question Id
                        designdocument_groupquestion_id = info.data.designdocumentgroupquestionid
                        sectiontype = info.data.sectiontype
                    }
                    )
                    .appendTo($el);

                container.append($el);
            },
        },
        {
            dataField: "grouptitle",
            caption: "Title",
        },
    ];
}


function delete_groupquestion(groupquestionid) {
    var url = url_delete_designdocument_groupquestion;
    var params = {
        "groupquestionid": groupquestionid
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


$(document).on("click", ".btn-save-groupquestion", function () {
    var url = url_insert_designdocument_groupquestion;

    var params = {
        "documentid": $("#documentid-text").val(),
        "groupquestionid": $("#groupquestionid-text").val(),
        "grouptitle": $("#groupquestion-title-text").val(),
        "sectiontype": $("#group-sectiontype-select").val(),
        "documentidcopy": "-1",
        "groupquestionidcopy": "-1"
    }

    if ($("#groupquestionid-text").val() == "-1") {
        if ($("#from-documentcopy-select").val() != 0) {
            params["documentidcopy"] = $("#from-documentcopy-select").val()
            params["groupquestionidcopy"] = $("#from-groupsectioncopy-select").val()
        }
    }

    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.success == "1") { 
            initialize_data();
            setTimeout(()=>{
                $(`#${$("#groupquestionid-text").val()}`).click()
                $("#groupquestion-modal").modal('hide')
                $.LoadingOverlay("hide")
            }, 1500)
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
});