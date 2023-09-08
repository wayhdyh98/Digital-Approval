var questiongroup = []
var answergroupid = []
var uuidgrouparr = []

$(document).ready(function () {
    console.log("JS Ready.");
});

// Button Click + Group Multirow
$(document).on("click", ".btn-plusgroup", function () {
    uuidcardgroup = uuidv4()
    uuidgroup = uuidv4()
    designdocumentgroupquestionid = $(this).data("groupquestionid")
    sectiontype = $(this).data("sectiontype")
    grouptitle = $(this).data("grouptitle")

    $(`div[data-basecardgroupid="${designdocumentgroupquestionid}"]`)
    .append($(`<div class="card flex-fill group-${designdocumentgroupquestionid}" data-cardgroupid="${designdocumentgroupquestionid}" data-componentbasecardgroup="${uuidcardgroup}">`)
    .append($(`<div class="card-body">`)
    .append($('<div class="input-group-prepend mb-3">')
    .append(`<button type="button" class="btn btn-danger btn-del-group" data-component="${uuidcardgroup}"><i class="fa-solid fa-minus"></i></button>`)
    .append(`<h4 class="mx-2 my-2">${grouptitle}</h4>`))
    .append(`<div class="groupid" data-groupid="${designdocumentgroupquestionid}" data-componentbasegroup="${uuidgroup}">`)))

    answergroupid.push({
        "uuid": uuidgroup
    })

    $('[name=arraygroupid]').val(JSON.stringify(answergroupid))

    initialize_question_multigroup(designdocumentgroupquestionid, uuidgroup)
});

async function initialize_question_multigroup(designdocumentgroupquestionid, uuidgroup) {
    for (var item of questiongroup) {
        if (item.designdocumentgroupquestionid == designdocumentgroupquestionid) {
            for (var itemquestion of item.question) {
                mandatory = ["", "", ""]
                uuid = uuidv4()
                uuidarea = uuidv4()
                note = ""
                style = ""

                uuidgrouparr.push({
                    "uuid": uuidarea,
                    "designdocumentquestionid": itemquestion.designdocumentquestionid,
                    "answer": "",
                    "counter": $(`.group-${itemquestion.designdocumentgroupquestionid}`).length+1
                })

                if (itemquestion.mandatory == 1) {
                    mandatory[0] = "required"
                    mandatory[1] = "*"
                    mandatory[2] = "<small class='text-danger font-italic'>(Wajib Diisi)</small>"
                }

                if (itemquestion.note != null && itemquestion.note != "") {
                    note = `<div id="note-area"><label style="color: #A5A5A5; font-size: 11px">${itemquestion.note}</label></div>`
                    style = "style='margin-bottom: 0px'"
                }

                $(`div[data-componentbasegroup="${uuidgroup}"]`).append(`<div class="mb-3 col questiondiv" id="questiondiv-${itemquestion.designdocumentquestionid}" data-area="${uuidarea}">`);
    
                $(`div[data-componentbasegroup="${uuidgroup}"] #questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<label class="form-label" ${style}>${itemquestion.question}${mandatory[1]}</label>`).append(mandatory[2]);

                $(`#questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(note)

                if (itemquestion.questioncondition == 1) {
                    if (itemquestion.questiontypecomponent == 2) {
                        $(`div[data-componentbasegroup="${uuidgroup}"] #questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<textarea class="form-control mb-2" data-questionid="${itemquestion.designdocumentquestionid}" data-uuidarea="${uuidarea}" name="${uuidgroup}-${itemquestion.designdocumentquestionid}" data-firstrow="${itemquestion.designdocumentquestionid}" ${mandatory[0]}></textarea>`);
                    } else {
                        $(`div[data-componentbasegroup="${uuidgroup}"] #questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<input type="text" class="form-control mb-2" data-questionid="${itemquestion.designdocumentquestionid}" data-uuidarea="${uuidarea}" name="${uuidgroup}-${itemquestion.designdocumentquestionid}" data-firstrow="${itemquestion.designdocumentquestionid}" ${mandatory[0]}/>`);
                    }
                } else if (itemquestion.questioncondition == 2) {
                    $(`div[data-componentbasegroup="${uuidgroup}"] #questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<select class="form-select flex-grow-1 mb-2" name="${uuidgroup}-${itemquestion.designdocumentquestionid}" data-questionid="${itemquestion.designdocumentquestionid}" data-componentvalue="${uuid}" data-uuidarea="${uuidarea}" data-firstrow="${itemquestion.designdocumentquestionid}" ${mandatory[0]}></select>`);

                    initialize_multichoice(itemquestion.designdocumentquestionid, uuid, false);
                } else {
                    $(`div[data-componentbasegroup="${uuidgroup}"] #questiondiv-${itemquestion.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<select class="form-select flex-grow-1 mb-2" name="${uuidgroup}-${itemquestion.designdocumentquestionid}" data-questionid="${itemquestion.designdocumentquestionid}" data-componentvalue="${uuid}" data-uuidarea="${uuidarea}" data-firstrow="${itemquestion.designdocumentquestionid}" ${mandatory[0]}></select>`);

                    initialize_selectquestion(itemquestion.designdocumentquestionid, itemquestion.questioncondition, uuid, false);
                }
            }
        }
    }
}

$(document).on("click", ".btn-del-group", function () {
    uuid = $(this).context.attributes["data-component"].value
    $(`[data-componentbasecardgroup="${uuid}"]`).remove()
});