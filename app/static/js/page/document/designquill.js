var quill
var getcontentorigin = {"forversion": [""], "forduplicate": [], "activeversion": 0}
var versionold = -1

Quill.register({
    'modules/better-table': quillBetterTable
}, true)

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    initialize_board()

    $.LoadingOverlay("hide");
})

$('#activeversion').change(function() {
    if(this.checked) {
        $("#iconversion").css("color", "#e8647c")
        $("#iconversion").removeClass("fa-lock-open")
        $("#iconversion").addClass("fa-lock")
        $("#activeversion").val("1")
    } else {
        $("#iconversion").css("color", "#495057")
        $("#iconversion").removeClass("fa-lock")
        $("#iconversion").addClass("fa-lock-open")
        $("#activeversion").val("0")
    }
    
    if ($("#activeversion").val() != $("#activeversion").attr("data-origin")) {
        $("#notif-save").show()
    } else {
        $("#notif-save").hide()
    }
})

function initialize_board(){
    $.LoadingOverlay("show");
    generate_editor()

    initialize_document()
    initialize_approver()
    initialize_groupquestion()
    initialize_version()
}

function generate_editor(){
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike',
            {'script': 'sub',}, 
            {'script': 'super',},
            {'color': [],}, 
            {'background': [],}, 'code',
        ],
        [{'font': [],}, {'size': ['small', false, 'large', 'huge'],}],
        ['link', 'image', 'video', 'formula'],
        ['blockquote', 'code-block', {'header': 1,},{'list': 'ordered',}, {'list': 'bullet',},],
        [{'indent': '-1',}, {'indent': '+1',}, {'direction': 'rtl',}, {'align': [],}],
        ['clean'],
    ];

    quill = new Quill('#editor', {
        modules: {
            toolbar: toolbarOptions,
            table: false,
            'better-table': {
                operationMenu: {
                    items: {
                        unmergeCells: {
                            text: 'Another unmerge cells name'
                        }
                    },
                    color: {
                        colors: ['green', 'red', 'yellow', 'blue', 'white'],
                        text: 'Background Colors:'
                    }
                }
            }
        },
        placeholder: 'Compose your document...',
        theme: 'snow'
    });

    if (layout == "1") {
        $("#testimoni").css("width", "29.7cm")
        $("#testimoni").css("height", "21cm")
        $(".modal-xl").css("max-width", "1400px")
    } else {
        $("#testimoni").css("height", "29.7cm")
        $("#testimoni").css("width", "21cm")
        $(".modal-xl").css("max-width", "1140px")
    }
}

function initialize_document() {
    var url = url_master_documents;

    function success_callback(data) {
        $("#thedocument").children().remove().end();
        $("#thedocument").append(`<option value=0>No</option>`)
        if (data.data.length > 0) {
            data.data.forEach(element => {
                $("#thedocument").append(`<option value=${element.masterdocid}>${element.name} (v${element.version})</option>`)
            })
        }
        $("#thedocument").find('option:first').prop('selected',true).change()
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$("#thedocument").change(function () {
    if ($(this).val() != 0) {
        $(".choose-design").show()
        initialize_version("no", true, $(this).val())
    } else {
        $(".choose-design").hide()
        $("#viewtemp").prop("disabled", true)
    }
})

function initialize_approver() {
    var url = url_master_approvals + "/" + $("#documentid-text").val();

    function success_callback(data) {
        $("#masterapprove").children().remove().end();
        data.data.forEach(element => {
            pictype = (element.pictype == "0" ? "Pemohon" : (element.pictype == "1" ? "Mengetahui" : "Menyetujui"))
            picname = (element.picname == null ? "Input by Document" : element.picname)
            $("#masterapprove").append(`<option value="${element.piclevel}.${element.picsublevel}">${element.piclevel}.${element.picsublevel} ${pictype} - ${picname}</option>`);
        });
        $("#masterapprove").find('option:first').prop('selected',true).change()
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function initialize_groupquestion() {
    var url = url_designdocument_groupquestions + "/" + $("#documentid-text").val();

    function success_callback(data) {
        if (data.data.length > 0) {
            $("#questiongroup").children().remove().end();
            data.data.forEach(element => {
                $("#questiongroup").append(`<option value="${element.grouptitle}" data-id="${element.designdocumentgroupquestionid}" data-sectiontype="${element.sectiontype}">${element.grouptitle}</option>`);
                initialize_question(element.designdocumentgroupquestionid, false, element.grouptitle, element.sectiontype)
            })
            $("#questiongroup").find('option:first').prop('selected',true).change()
        } else {
            Swal.fire(
                'Group Question not found!',
                'Please set the group question first!',
                'error'
            )
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$("#questiongroup").change(function () {
    $.LoadingOverlay("show");
    var sectiontype = $(this).find(':selected').attr('data-sectiontype')
    if (sectiontype == 1) {
        $("#question").attr("disabled", true)
        $("#rowmultibutton").show()
        $("#rowsinglebutton").hide()      
    } else {
        $("#rowmultibutton").hide()
        $("#question").attr("disabled", false)
        $("#rowsinglebutton").show()
    }
    initialize_question($(this).find(':selected').attr('data-id'), true, null, sectiontype)
})

function initialize_question(designdocumentgroupquestionid, foroption = true, grouptitle = null, sectiontype = 0) {
    var url = url_designdocument_questions + "/" + $("#documentid-text").val() + "/" + designdocumentgroupquestionid;

    function success_callback(data) {
        if (data.data.length > 0) {
            var isThereMultirow = data.data.find(x => x.questiontype == 1)

            if (foroption) {
                $("#question").children().remove().end();
            }
            
            data.data.forEach(element => {
                if (foroption) {
                    questiontype = (element.questiontype == 0 ? "Single" : "Multirow")
                    isThereMultirow = (element.questiontype == 0 ? false : true)
                    $("#question").append(`<option value="${element.question}" data-questionid="${element.designdocumentquestionid}" data-questiontype="${element.questiontype}" data-questioncondition="${element.questioncondition}" data-groupsection="${sectiontype}">${element.question} - ${questiontype}</option>`)
                } else {
                    if (element.questiontype == 1 || sectiontype == 1) {
                        var groupquestionindex = multirow.findIndex(i => (i.designdocumentgroupquestionid == designdocumentgroupquestionid))
                        if (groupquestionindex == -1) {
                            multirow.push({
                                designdocumentgroupquestionid: designdocumentgroupquestionid,
                                grouptitle: grouptitle,
                                designdocumentquestion: [{id: element.designdocumentquestionid, question:element.question}]
                            })
                        } else {
                            var questionindex = multirow[groupquestionindex]['designdocumentquestion'].findIndex(i => (i.id == element.designdocumentquestionid))
                            if (questionindex == -1) {
                                multirow[groupquestionindex]['designdocumentquestion']
                                .push({id: element.designdocumentquestionid, question:element.question})
                            }
                        }
                    }
                }
            })

            if (foroption) {
                if (isThereMultirow != false) {
                    $("#question").append(`<option value="multirow" data-questiontype="2" data-groupsection="0">Question Multirow</option>`)
                    $("#question option[data-questiontype='1']").hide()
                }

                if (sectiontype == 0) {
                    $("#question").find('option:first').prop('selected',true).change()
                }
            }
            $.LoadingOverlay("hide");
        } else {
            Swal.fire(
                'Question is not found',
                'Please set the question first!',
                'error'
            )
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$("#question").change(function () {
    $.LoadingOverlay("show");
    var questiontype = $(this).find(':selected').attr('data-questiontype')
    if (questiontype == 1) {
        $("#rowmultibutton").show()
        $("#rowsinglebutton").hide()
        $.LoadingOverlay("hide");
    } else {
        $("#rowmultibutton").hide()
        $("#rowsinglebutton").show()
        $.LoadingOverlay("hide");
    }
})

function initialize_version(todolasttime = "no", forduplicate = false, documentid = $("#documentid-text").val()) {
    var url = url_designdocument + "/" + documentid;

    function success_callback(data) {
        if (!forduplicate) {
            getcontentorigin["forversion"] = [""]
            getcontentorigin["activeversion"] = 0
            $("#version").children().remove().end();

            $("#version").append(`<option value=0 data-designdocumentid=0 data-contentorigin=0>New Version</option>`)
            if (data.data.length > 0) {
                $("#activeversion").prop("disabled", false)

                var idx = 1
                
                data.data.forEach(element => {
                    $("#version").append(`<option value=${element.version} data-designdocumentid="${element.designdocumentid}" data-contentorigin=${idx}>${$("#documentversion-text").val().charAt(0)}.${element.version}</option>`)    
                    getcontentorigin["forversion"].push(element.contentorigin)
 
                    if (idx == 1) getcontentorigin["activeversion"] = element.activeversiondocument

                    idx++
                })
            } else {
                $("#activeversion").prop("disabled", true)
                $('#activeversion').prop('checked', true).change()
            }

            if (todolasttime != "no") {
                $("#version").find(`option[value="${todolasttime}"]`).prop('selected',true).change()
            } else {
                $("#version").find('option:first').prop('selected',true).change()
            }
        } else {
            getcontentorigin["forduplicate"] = []
            $("#thedesign").children().remove().end();
            if (data.data.length > 0) {
                $("#viewtemp").prop("disabled", false)
                var idx = 0

                data.data.forEach(element => {
                    $("#thedesign").append(`<option value=${element.version} data-designdocumentid="${element.designdocumentid}" data-contentorigin=${idx}>${$("#documentversion-text").val()}.${element.version}</option>`)
                    getcontentorigin["forduplicate"].push(element.contentorigin)
                    idx++
                })
            } else {
                $("#viewtemp").prop("disabled", true)
                $("#thedesign").append(`<option value=0 data-designdocumentid=0 data-contentorigin=0>No Design</option>`)
            }
            $("#thedesign").find('option:first').prop('selected',true).change()
        }

        $.LoadingOverlay("hide");
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$("#version").change(function () {
    if (parseInt($("#version").val()) == getcontentorigin["activeversion"]) {
        $('#activeversion').removeData('data-origin').attr('data-origin', "1")
        $('#activeversion').prop('checked', true).change()
    } else {
        $('#activeversion').removeData('data-origin').attr('data-origin', "0")
        $('#activeversion').prop('checked', false).change()
    }

    var idx = $(this).find(':selected').attr('data-contentorigin')

    if (versionold != -1 && idx == 0) {
        quill.root.innerHTML = getcontentorigin["forversion"][idx]
        destory_editor("#editor")
        generate_editor()
    } else if (versionold != -1 && idx != 0) {
        destory_editor("#editor")
        generate_editor()
        quill.root.innerHTML = getcontentorigin["forversion"][idx]
    }
})

$("#version").click(function () {
    versionold = $(this).find(':selected').attr('data-contentorigin')
})

function destory_editor(selector){
    if($(selector)[0])
    {
        var content = $(selector).find('.ql-editor').html();
        $(selector).html(content);

        $(selector).siblings('.ql-toolbar').remove();
        $(selector + " *[class*='ql-']").removeClass (function (index, css) {
           return (css.match (/(^|\s)ql-\S+/g) || []).join(' ');
        });

        $(selector + "[class*='ql-']").removeClass (function (index, css) {
           return (css.match (/(^|\s)ql-\S+/g) || []).join(' ');
        });
    }
    else
    {
        console.error('editor not exists');
    }
}

function set_preview() {
    var content = quill.root.innerHTML
    reArrangePosition(content)
    var _html = `<style>
                .noBorder {
                    border:none !important;
                }
                table {
                    table-layout: auto !important;
                }
                </style>`
    _html += replaceTable(content)

    $('#testimoni').html(_html)

    $(".quill-better-table").each(function () {
        const tbody = $(this).children("tbody:first")
        const tr = $(tbody).children("tr:first")
        const td = $(tr).children("td:first")
        const p = $(td).children("p:first").text()

        if (p == "--borderless") {
            $(this).addClass("noBorder")
            $("tr", this).css("border", "none")
            $("td", this).css("border", "none")
            $(tr).remove()
        } else {
            $(this).addClass("withBorder")
            $(this).css("border", "1px solid black")
            $(tr).remove()
        }
    })

    quill.root.innerHTML = content
}

$(document).on("click", "#viewtemp", function () {
    var idx = $("#thedesign").find(':selected').attr('data-contentorigin')
    quill.root.innerHTML = getcontentorigin["forduplicate"][idx]
})

$(document).on("click", "#btn-preview", function () {
    set_preview()
})

$(document).on("click", ".btn-insert-table", function () {
    var placeholder = $(this).context.attributes["data-insert"].value
    var tableModule = quill.getModule('better-table')
    tableModule.insertTable(2, 2)

    var position = quill.getSelection(true)
    quill.insertText(position, placeholder)
})

$(document).on("click", ".btn-insert", function () {
    var idbutton = $(this).attr('id')
    var placeholder = $(this).context.attributes["data-insert"].value
    var position = quill.getSelection(true)

    switch(idbutton) {
        case "approver-title":
        case "approver-name":
        case "approver-signature":
            placeholder = placeholder.replace("Level", $("#masterapprove").val())
            break
        case "btn-question":
        case "btn-questionanswer":
            placeholder = placeholder.replace("Question", $("#question").val())
            break
        case "btn-card":
        case "btn-table":
            var childOptions = ""
            $("#question option").each(function () {
                var questiontype = $(this).context.attributes["data-questiontype"].value
                var groupsection = $(this).context.attributes["data-groupsection"].value
                if (questiontype == 1 || groupsection == 1) {
                    childOptions += `\n"${$(this).val()}",@${$(this).val()};`
                }
            })
            placeholder = `##${placeholder}_${$("#questiongroup option:selected").text().split("-")[0].trim()}${childOptions}##`
            break
        default:
            placeholder = placeholder
    }
    
    quill.insertText(position, placeholder)
})

$(document).on("click", "#btn-design", function () {
    var title = "Are you sure want to save it?"
    var text = "Please check again if you not sure"
    var denyButton = false
    var denyText = ""
    var confirmText = "Save it."
    var contentorigin = quill.root.innerHTML
    var message = "Saved"

    if ($("#version").val() != 0) {
        title = `Are you sure want to update in version ${$("#version").val()}?`
        text = "You won't be able to revert this!"
        denyButton = true
        denyText = "Save as new version."
        confirmText = "Update it."
        message = "Updated"
    }

    var params = {
        "documentid": $("#documentid-text").val(),
        "contentdocument": "",
        "contentorigin": contentorigin,
        "version": "",
        "activeversiondocument": $("#activeversion").val(),
        "designdocumentid": ""
    }

    Swal.fire({
        title: title,
        text: text,
        icon: 'warning',
        showDenyButton: denyButton,
        showCancelButton: true,
        confirmButtonText: confirmText,
        denyButtonText: denyText,
      }).then((result) => {
        if (result.isConfirmed) {
            set_preview()

            if ($("#version").val() != 0) {
                params["version"] = $("#version").val()
                params["contentdocument"] = $("#testimoni").html()
                params["designdocumentid"] = $("#version").find(':selected').attr("data-designdocumentid")
            } else {
                params["version"] = 0
                params["contentdocument"] = $("#testimoni").html()
            }
            
            insert_designdocument(params, message)
        } else if (result.isDenied) {
            set_preview()

            params["version"] = 0
            params["contentdocument"] = $("#testimoni").html()

            insert_designdocument(params, message)
        }
      })
})

function insert_designdocument(params, message) {
    var url = url_insert_designdocument;

    $.LoadingOverlay("show");
    function success_callback(data) {
        $.LoadingOverlay("hide");
        Swal.fire({
            title: `Design Has Been ${message}!`,
            icon: 'success'
        })
        initialize_version($("#version").val())
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback)
}