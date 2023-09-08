var multichoice = [];

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    initialize_component();

    $.LoadingOverlay("hide");
});

$("#btn-design").click(function() {
    window.open(`/document/design/designquill/${$("#documentid-text").val()}`, '_blank')
})


function initialize_component(params = {designdocumentquestionid: -1, questiontype: "0", question: "Change this question.", masterdocid: $("#documentid-text").val(), questioncondition: "1", questiontypecomponent: "1", mandatory: "0", note: null}) {
    // Refresh multichoice array

    multichoice = []
    refresh_component_preview("1");
    $("#question-preview-area-select").hide(100);
    $(".mandatory-sign").hide();
    $("#freetext-area").show(100);
    $("#multichoice-area").hide(100);
    $("#masterview-area").hide(100);

    // Set default value
    $("#question-questiontype-select").val(params["questiontype"]).change();
    $("#question-question-text").val(params["question"]);
    $("#label-question").text(params["question"]);   
    $("#question-note-text").val(params.note)
    check_note_length(params.note)
    
    $("#question-questioncondition-select").val(params["questioncondition"]).change();
    $("#freetext-component-select").val(params["questiontypecomponent"]).change();
    if (params["mandatory"] == "0") {
        $('#question-mandatory-check').prop('checked', false);
    } else {
        $('#question-mandatory-check').prop('checked', true);
    }

    if (sectiontype == 1) {
        $("#question-questiontype-select").attr("disabled", true)
    } else {
        $("#question-questiontype-select").attr("disabled", false)
    }

    $('#question-documentid-text').attr("data-question-documentid-text", params["masterdocid"]);
    $('#questionid-text').attr("data-questionid-text", params["designdocumentquestionid"]);
}


function initialize_component_edit(params) {
    initialize_component(params)
    // Set multichoice option from DB
    initialize_data_multichoice(params["designdocumentquestionid"])
}


function removeDataAttribute(){
    $("#question-multichoice-select option").remove()
    $('#questionid-text').removeData("questionid-text");
    $('#question-documentid-text').removeData("question-documentid-text");
}


/* define the column of the grid  */
browse_column_question = function () {
    return [
        {
            caption: "#",
            width: 150,
            fixed: true,
            headerCellTemplate: function (header, info) {
                $('<a>New</a>')
                    .attr('href', '#')
                    .click(function () {
                        removeDataAttribute()
                        initialize_component();
                        $("#question-modal").modal("show");
                    })
                    .appendTo(header);
            },
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                $('<a class="btn btn-sm btn-dark col"><i class="fa fa-pen" aria-hidden="true"></i> Edit</a>')
                    .attr('href', '#')
                    .click(function () {
                        removeDataAttribute()
                        initialize_component_edit(info.data)
                        $("#question-modal").modal("show");
                    }
                    )
                    .appendTo($el);
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
                                delete_question(info.data.designdocumentquestionid)
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
            dataField: "question",
            caption: "Question",
        },
        {
            dataField: "questiontype",
            caption: "Type",
            cellTemplate: function (container, options) {
                if (options.value == "1") {
                    $('<h6><span class="col">Multiple</span></h6>').appendTo(container);
                }
                else if (options.value == "0") {
                    $('<h6><span class="col">Single</span></h6>').appendTo(container);
                }
            },
        },
        {
            dataField: "questioncondition",
            caption: "Condition",
            cellTemplate: function (container, options) {
                if (options.value == "1") {
                    $('<h6><span class="col">Free Text</span></h6>').appendTo(container);
                }
                else if (options.value == "2") {
                    $('<h6><span class="col">Multiple Custom</span></h6>').appendTo(container);
                }
                else {
                    $(`<h6><span class="col">${options.data.questionconditionname}</span></h6>`).appendTo(container);
                }
            },
        },
        {
            dataField: "mandatory",
            caption: "Is Mandatory?",
            alignment: 'center',
            cellTemplate: function (container, options) {
                if (options.value == "1") {
                    $('<h6><span class="badge badge-success col">Mandatory</span></h6>').appendTo(container);
                }
                else if (options.value == "0") {
                    $('<h6><span class="badge badge-danger col">Not Mandatory</span></h6>').appendTo(container);
                }
            },
        },
    ];
}

function delete_question(designdocumentquestionid) {
    var url = url_delete_designdocument_question;
    
    var params = {
        "questionid": designdocumentquestionid,
    }

    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.success == "1") {
            initialize_data_question(designdocument_groupquestion_id);
        }
        $.LoadingOverlay("hide");
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
}


/* question text on change */
$('#question-question-text').on('keyup', function () {
    $("#label-question").text(this.value);
});
$('#question-question-note-text').on('keyup', function () {
    $("#label-question-note").text(this.value);
});
/* question text on change */

// question note on change
$('#question-note-text').on('keyup', function () {
    check_note_length(this.value)
})

function check_note_length(str) {
    $("#label-question-note").text(str);
    if ($('#question-note-text').val().length == 0) {
        $('#note-area').hide()
        $('#label-question').css('margin-bottom', '8px');
    } else {
        $('#note-area').show()
        $('#label-question').css('margin-bottom', '0px');
    }
}


/* question condition select on change */
function refresh_component_preview_select(statuscondition) {
    if (statuscondition == 1) {
        var $options = $("#question-multichoice-select > option").clone();
        $('#question-preview-copy-select').children().remove().end();
        $('#question-preview-copy-select').append($options);
    }
    else if (statuscondition == 2) {
        // copy from master view select
        var $options = $("#question-masterview-select > option").clone();
        $('#question-preview-copy-select').children().remove().end();
        $('#question-preview-copy-select').append($options);
    }

    $("#question-preview-area").hide(100);
    $("#question-preview-area-select").show(100);
}

function questioncondition_onchange(value, statuscondition) {
    // status condition
    $("#freetext-area").hide(100);
    $("#multichoice-area").hide(100);
    $("#masterview-area").hide(100);
    if (statuscondition == 0) { // free text
        $("#freetext-area").show(100);
        $("#question-preview-area").show(100);
        $("#question-preview-area-select").hide(100);
    }
    else if (statuscondition == 1) { // multi choice
        // show the data
        // TODO: create select multichoice
        $("#multichoice-area").show(100);
        refresh_component_preview_select(statuscondition);
    }
    else if (statuscondition == 2) { // master
        // show the data
        $.LoadingOverlay("show");
        function success_callback(data) {
            if (data.success == "1") {
                $('#question-masterview-select').children().remove().end();
                data.data.forEach(element => {
                    $("#question-masterview-select").append('<option value=' + element.code + '>' + element.value + '</option>');
                });
                $("#masterview-area").show(100);
                refresh_component_preview_select(statuscondition);
            }
            $.LoadingOverlay("hide");
        }
        function error_callback() {
            $.LoadingOverlay("hide");
        }
        var url = url_designdocument_questioncondition + "/" + $("#documentid-text").val() + "/" + value + "/" + statuscondition;
        page.read_data(url, null, 'GET', success_callback, error_callback);
    }
}


$('#question-questioncondition-select').on('change', function () {
    questioncondition_onchange(this.value, $(this).find(':selected').attr('data-statuscondition'));
});
/* question condition select on change */


/* question component select on change */
function refresh_component_preview(type_component) {
    if (type_component == "1") {
        script_component = '<input type="text" class="form-control">';
    }
    else if (type_component == "2") {
        script_component = '<textarea class="form-control" row="5"></textarea>';
    }
    $("#question-preview-area").html(script_component);
}
$('#freetext-component-select').on('change', function () {
    refresh_component_preview(this.value);
});
/* question component select on change */


/* mandatory on change */
$('#question-mandatory-check').on('change', function () {
    var value = $(this).is(":checked");
    if (value) {
        $(".mandatory-sign").show();
    }
    else {
        $(".mandatory-sign").hide();
    }
});
/* mandatory on change */


/* multichoice */
function clone_multichoice() {
    var $options = $("#question-multichoice-select > option").clone();
    $('#question-preview-copy-select').children().remove().end();
    $('#question-preview-copy-select').append($options);
}

$(document).on("click", ".btn-add-multichoice", function () {
    var value = $("#question-multichoice-text").val();
    var data = {
        "code": uuidv4(),
        "value": value
    }
    multichoice.push(data);
    $("#question-multichoice-select").append('<option value=' + data.code + '>' + data.value + '</option>');
    $("#question-multichoice-text").val("");
    $("#question-multichoice-select").val(data.code);
    clone_multichoice();
});

$(document).on("click", ".btn-remove-multichoice", function () {
    var code = $("#question-multichoice-select").val();

    var index = -1;
    var pos = 0;
    multichoice.forEach(element => {
        if (element.code == code) {
            index = pos;
        }
        pos++;
    });
    if (index !== -1) {
        multichoice.splice(index, 1);
    }

    $('#question-multichoice-select').children().remove().end();
    multichoice.forEach(element => {
        $("#question-multichoice-select").append('<option value=' + element.code + '>' + element.value + '</option>');
    });
    clone_multichoice();
});
/* multichoice */


/* save */
$(document).on("click", ".btn-save-question", function () {
    var url = url_insert_designdocument_question;

    // check for mandatory
    var mandatory_check = "0";
    if ($('#question-mandatory-check').is(":checked"))
    {
        mandatory_check = "1";
    }

    var params = {
        "questionid": $('#questionid-text').data('questionid-text'),
        "groupquestionid": $('#question-groupquestionid-text').data('question-groupquestionid-text'),
        "documentid": $('#question-documentid-text').data('question-documentid-text'),
        "question": $("#question-question-text").val(),
        "questiontype": $("#question-questiontype-select").val(),
        "questioncondition": $("#question-questioncondition-select").val(),
        "mandatory": mandatory_check,
        "note": $("#question-note-text").val(),
        "questiontypecomponent": $("#freetext-component-select").val(),
        "multichoice": multichoice
    }

    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.success == "1") {
            initialize_data_question(designdocument_groupquestion_id);
            $("#question-modal").modal('hide');
        }
        $.LoadingOverlay("hide");
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
});
/* save */