var arrayquestionid = []
var selectoptiondata = {'2': [], '3': [], '4': [], '5': []}
var arrayuuid = []
var uuid = ''

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});

function initialize_data() {
    var url = url_designdocument_groupquestions + "/" + $("#documentid").val()
    $.LoadingOverlay("show");
    async function success_callback(data) {
        if (data.data.length > 0) {
            var res = await initialize_grupquestion(data.data)
            setTimeout(()=>{ check_answer() }, 2000)
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

function check_answer() {
    var url = url_answer_submissions_fillformrequest + "/" + $("#requestapprovalid").val()

    async function success_callback(data) {
        if (data.data.length > 0) {
            var res = await set_answer(data.datasinglegroup)
            var res2 = await set_answergroup(data.arr2)
            var res3 = await set_answermultirow(data.datamultirow)
            var res4 = await set_answermultirowuuid()
        } else {
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

async function set_answer(params) {
    return new Promise((resolve, reject) => {
        for (var element of params) {
            if (element.questioncondition == 1) {
                if (element.questiontypecomponent == 2) {
                    $(`textarea[data-questionid="${element.designdocumentquestionid}"]`).val(element.answer)
                } else {
                    $(`input[data-questionid="${element.designdocumentquestionid}"]`).val(element.answer)
                }
            } else {
                console.log(element.answer)
                $(`select[data-questionid="${element.designdocumentquestionid}"]`).val(element.answer).change()
            }
        }
        setTimeout(() => resolve("Done set single question answer"), 1000)
    })
}

async function set_answergroup(params) {
    return new Promise((resolve, reject) => {
        var counter = 1
        for (var element of params) {
            var savedgroupid = element[0].answergroupid
            for (var childel of element) {
                if (element.length > 2 && savedgroupid != childel.answergroupid) {
                    counter += 1
                    $(`button[data-groupquestionid="${childel.designdocumentgroupquestionid}"]`).click()
                }
                if ($(`.group-${childel.designdocumentgroupquestionid}`).length == 0) {
                    if (childel.questioncondition == 1) {
                        if (childel.questiontypecomponent == 2) {
                            $(`textarea[data-questionid="${childel.designdocumentquestionid}"]`).val(childel.answer)
                            counter = 1
                        } else {
                            $(`input[data-questionid="${childel.designdocumentquestionid}"]`).val(childel.answer)
                            counter = 1
                        }
                    } else {
                        $(`select[data-questionid="${childel.designdocumentquestionid}"]`).val(childel.answer).change()
                        counter = 1
                    }
                } else {
                    objIndex = uuidgrouparr.findIndex((obj => obj.counter == counter && obj.designdocumentquestionid == childel.designdocumentquestionid))
                    if (objIndex != -1) {
                        uuidgrouparr[objIndex].answer = childel.answer
                    }
                }
                savedgroupid = childel.answergroupid
            }
        }

        setTimeout(() => resolve("Done set multi group answer"), 2000)
    })
}

async function set_answermultirow(data) {
    return new Promise((resolve, reject) => {
        for (var x of data) {
            if (x.length > 0) {
                var counter = 1
                for (var element of x) {
                    if (element.questioncondition == 1) {
                        if (element.questiontypecomponent == 2) {
                            if ($(`.multi-textarea-${element.designdocumentgroupquestionid}`).length == 0) {
                                $(`textarea[data-firstrow="${element.designdocumentquestionid}"]`).val(element.answer)

                                if (x.length > 1) {
                                    $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                                }
                            } else {
                                arrayuuid.push({
                                    "uuid": uuid,
                                    "answer": element.answer
                                })
                                if (counter < x.length) {
                                    $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                                }
                            }
                        } else {
                            if ($(`.multi-inputtext-${element.designdocumentgroupquestionid}`).length == 0) {
                                $(`input[data-firstrow="${element.designdocumentquestionid}"]`).val(element.answer)

                                if (x.length > 1) {
                                    $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                                }
                            } else {
                                arrayuuid.push({
                                    "uuid": uuid,
                                    "answer": element.answer
                                }) 
                                if (counter < x.length) {
                                    $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                                }
                            }
                        }
                    } else {
                        if ($(`.multi-select${element.questioncondition}-${element.designdocumentgroupquestionid}`).length == 0) {
                            $(`select[data-firstrow="${element.designdocumentquestionid}"]`).val(element.answer).change()
                            if (x.length > 1) {
                                $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                            }
                        } else {
                            arrayuuid.push({
                                "uuid": uuid,
                                "answer": element.answer
                            })
    
                            if (counter < x.length) {
                                $(`button[data-questionid="${element.designdocumentquestionid}"]`).click()
                            }
                        }
                    }
                    counter += 1
                }
            }
        }
        setTimeout(() => resolve("Done set first row and click button multirow"), 2000)
    })
}

async function set_answermultirowuuid() {
    return new Promise((resolve, reject) => {
        console.log(uuidgrouparr)
        for (var element of arrayuuid) {
            $(`[data-componentvalue="${element.uuid}"]`).val(element.answer).change()
        }

        for (var element of uuidgrouparr) {
            $(`[data-uuidarea="${element.uuid}"]`).val(element.answer).change()
        }
        setTimeout(() => resolve("Done load from uuid"), 2000)
        $.LoadingOverlay("hide")
    })
}

async function initialize_grupquestion(params) {
    return new Promise((resolve, reject) => {
        $("#fillform").children().remove().end()
        for (var element of params) {
            uuidcardgroup = uuidv4()
            uuidgroup = uuidv4()

            $("#fillform").append($(`<div data-basebuttongroupid="${element.designdocumentgroupquestionid}">`))

            $(`div[data-basebuttongroupid="${element.designdocumentgroupquestionid}"]`)
            .append($(`<div data-basecardgroupid="${element.designdocumentgroupquestionid}">`)
            .append($(`<div class="card flex-fill" data-cardgroupid="${element.designdocumentgroupquestionid}" data-componentbasecardgroup="${uuidcardgroup}">`)
            .append($('<div class="card-body">')
            .append(`<div class="groupid" data-groupid="${element.designdocumentgroupquestionid}" data-componentbasegroup="${uuidgroup}"><h4>${element.grouptitle}</h4></div>`))))
    
            initialize_question(element.designdocumentgroupquestionid, element.sectiontype, uuidgroup);

            if (element.sectiontype == 1) {
                $(`div[data-basebuttongroupid="${element.designdocumentgroupquestionid}"]`).append($(`<div class="row mb-3 mx-0 button-area" id="btnarea-${element.designdocumentgroupquestionid}" style="background-color: #E0E0E0">`).append($('<div class="col-md-12 text-center">').append(`<button type="button" class="btn btn-primary col-1 btn-plusgroup my-2" id="btnplusgroup-${element.designdocumentgroupquestionid}" data-grupareaid="${uuidgroup}" data-groupquestionid="${element.designdocumentgroupquestionid}" data-sectiontype="${element.sectiontype}" data-grouptitle="${element.grouptitle}"><i class="fa-solid fa-plus"></i></button>`)))

                answergroupid.push({
                    "uuid": uuidgroup
                })
                
            }
            $('[name=arraygroupid]').val(JSON.stringify(answergroupid))
        }
        resolve("Done Load Group")
    })
}

async function initialize_question(designdocumentgroupquestionid, sectiontype = 0, uuidgroup) {
    var url = url_designdocument_questions + "/" + $("#documentid").val() + "/" + designdocumentgroupquestionid;

    function success_callback(data) {
        if (data.data.length > 0) {
            data.data.forEach(element => {
                mandatory = ["", "", ""]
                uuid = uuidv4()
                uuidarea = uuidv4()
                note = ""
                style = ""
                inputname = element.designdocumentquestionid

                if (element.mandatory == 1) {
                    mandatory[0] = "required"
                    mandatory[1] = "*"
                    mandatory[2] = "<small class='text-danger font-italic'>(Wajib Diisi)</small>"
                }

                if (sectiontype == 1) {
                    inputname = `${uuidgroup}-${element.designdocumentquestionid}`
                }

                if (element.note != null && element.note != "") {
                    note = `<div id="note-area"><label style="color: #A5A5A5; font-size: 11px">${element.note}</label></div>`
                    style = "style='margin-bottom: 0px'"
                }

                $(`div[data-groupid="${designdocumentgroupquestionid}"][data-componentbasegroup="${uuidgroup}"]`).append(`<div class="mb-3 col questiondiv" id="questiondiv-${element.designdocumentquestionid}" data-area="${uuidarea}">`);
    
                $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<label class="form-label" ${style}>${element.question}${mandatory[1]}</label>`).append(mandatory[2]);

                $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(note)

                if (element.questioncondition == 1) {
                    if (element.questiontypecomponent == 2) {
                        $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<textarea class="form-control mb-2" data-questionid="${element.designdocumentquestionid}" name="${inputname}" data-firstrow="${element.designdocumentquestionid}" ${mandatory[0]}></textarea>`);
                    } else {
                        $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<input type="text" class="form-control mb-2" data-questionid="${element.designdocumentquestionid}" name="${inputname}" data-firstrow="${element.designdocumentquestionid}" ${mandatory[0]}/>`);
                    }
                } else if (element.questioncondition == 2) {
                    $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<select class="form-select flex-grow-1 mb-2" name="${inputname}" data-questionid="${element.designdocumentquestionid}" data-component="${uuid}" data-componentvalue="${uuid}" data-firstrow="${element.designdocumentquestionid}" ${mandatory[0]}></select>`);
                    initialize_multichoice(element.designdocumentquestionid, uuid);
                } else {
                    $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<select class="form-select flex-grow-1 mb-2" name="${inputname}" data-questionid="${element.designdocumentquestionid}" data-component="${uuid}" data-componentvalue="${uuid}" data-firstrow="${element.designdocumentquestionid}" ${mandatory[0]}></select>`);
                    initialize_selectquestion(element.designdocumentquestionid, element.questioncondition, uuid);
                }
    
                if (element.questiontype == 1) {
                    $(`#questiondiv-${element.designdocumentquestionid}[data-area="${uuidarea}"]`).append($(`<div class="row my-2 mx-0 button-area" id="btnarea-${element.designdocumentquestionid}" style="background-color: #f7f9fc">`).append($('<div class="col-md-12 text-center">').append(`<button type="button" class="btn btn-primary col-1 btn-plus my-2" id="btnplus-${element.designdocumentquestionid}" data-areaid="${uuidarea}" data-groupquestionid="${designdocumentgroupquestionid}" data-questionid="${element.designdocumentquestionid}" data-question="${element.question}" data-questioncondition=${element.questioncondition} data-questiontypecomponent=${element.questiontypecomponent} data-note="${element.note}" data-mandatory1="${mandatory[0]}" data-mandatory2="${mandatory[1]}" data-mandatory3="${mandatory[2]}"><i class="fa-solid fa-plus"></i></button>`)))
                }
    
                arrayquestionid.push({
                    questionid: element.designdocumentquestionid,
                    question: element.question,
                    groupquestionid: designdocumentgroupquestionid,
                    questiontype: element.questiontype,
                    sectiontype: sectiontype
                })
            })

            if (sectiontype == 1) {
                questiongroup.push({
                    designdocumentgroupquestionid: designdocumentgroupquestionid,
                    question: data.data
                })
            }

            $('[name=arrayquestionid]').val(JSON.stringify(arrayquestionid));
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

function initialize_multichoice(designdocumentquestionid, uuid, firsttime = true) {
    if (firsttime) {
        var url = url_designdocument_questions_multichoice + "/" + designdocumentquestionid;

        function success_callback(data) {
            selectoptiondata[2] = []
            $(`select[data-componentvalue="${uuid}"]`).children().remove().end();
            data.data.forEach(element => {
                $(`select[data-componentvalue="${uuid}"]`).append(`<option value="${element.code}">${element['[value]']}</option>`)
                selectoptiondata[2].push({code: element.code, value:element['[value]']})
            })
        }

        function error_callback() {
            $.LoadingOverlay("hide");
        }

        page.read_data(url, null, 'GET', success_callback, error_callback);
    } else {
        $(`select[data-componentvalue="${uuid}"]`).children().remove().end();
        selectoptiondata[2].forEach(element => {
            $(`select[data-componentvalue="${uuid}"]`).append(`<option value="${element.code}">${element.value}</option>`)
        })
    }
    
}

function initialize_selectquestion(designdocumentquestionid, questioncondition, uuid, firsttime = true) {
    if (firsttime) {
        var url = `${url_designdocument_questioncondition}/${$("#documentid").val()}/${questioncondition}/2`;
        function success_callback(data) {
            if (data.success == "1") {
                selectoptiondata[questioncondition] = []
                $(`select[data-componentvalue="${uuid}"]`).children().remove().end();
                data.data.forEach(element => {
                    $(`select[data-componentvalue="${uuid}"]`).append(`<option value="${element.code}">${element.value}</option>`)
                    selectoptiondata[questioncondition].push({code: element.code, value:element.value})
                })
            }
        }
        function error_callback() {
            $.LoadingOverlay("hide");
        }
        
        page.read_data(url, null, 'GET', success_callback, error_callback);
    } else {
        $(`select[data-componentvalue="${uuid}"]`).children().remove().end();
        selectoptiondata[questioncondition].forEach(element => {
            $(`select[data-componentvalue="${uuid}"]`).append(`<option value="${element.code}">${element.value}</option>`)
        })
    }
}

// Button Click + Question Multirow
$(document).on("click", ".btn-plus", function () {
    uuid = uuidv4()
    uuidarea = $(this).data("areaid")
    designdocumentquestionid = $(this).data("questionid")
    designdocumentgroupquestionid = $(this).data("groupquestionid")
    question = $(this).data("question")
    questioncondition = $(this).data("questioncondition")
    questiontypecomponent = $(this).data("questiontypecomponent")
    note = $(this).data("note")
    mandatory1 = $(this).data("mandatory1")
    mandatory2 = $(this).data("mandatory2")
    mandatory3 = $(this).data("mandatory3")
    style = ''

    if (mandatory3.length > 0) {
        mandatory3 = `<small class="text-danger font-italic" data-component="${uuid}">(Wajib Diisi)</small>`
    }

    if (note != null && note != "") {
        note = `<div id="note-area" data-component="${uuid}"><label style="color: #A5A5A5; font-size: 11px">${note}</label></div>`
        style = "style='margin-bottom: 0px'"
    }
    
    $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`).append(`<label class="form-label" data-component="${uuid}" ${style}>${question}${mandatory2}</label>`).append(mandatory3).append($(`#btnarea-${designdocumentquestionid}`));

    $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`).append(note)

    if (questioncondition == 1) {
        if (questiontypecomponent == 2) {
            $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`)
            .append($(`<div class="input-group mb-3" data-component="${uuid}" id="btndel-${designdocumentquestionid}">`)
            .append($('<div class="input-group-prepend">').append(`<button type="button" class="btn btn-danger btn-del" data-component="${uuid}"><i class="fa-solid fa-minus"></i></button>`))
            .append(`<textarea class="form-control multi-textarea-${designdocumentgroupquestionid}" data-componentvalue="${uuid}" data-questionid="${designdocumentquestionid}" name="${designdocumentquestionid}" ${mandatory1}></textarea>`))
            .append($(`#btnarea-${designdocumentquestionid}`));
        } else {
            $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`)
            .append($(`<div class="input-group mb-3" data-component="${uuid}" id="btndel-${designdocumentquestionid}">`)
            .append($('<div class="input-group-prepend">').append(`<button type="button" class="btn btn-danger btn-del" data-component="${uuid}"><i class="fa-solid fa-minus"></i></button>`))
            .append(`<input type="text" class="form-control multi-inputtext-${designdocumentgroupquestionid}" data-componentvalue="${uuid}" data-questionid="${designdocumentquestionid}" name="${designdocumentquestionid}" ${mandatory1}/>`))
            .append($(`#btnarea-${designdocumentquestionid}`));
        }
    } else if (questioncondition == 2) {
        $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`)
        .append($(`<div class="input-group mb-3" data-component="${uuid}" id="btndel-${designdocumentquestionid}">`)
        .append($('<div class="input-group-prepend">').append(`<button type="button" class="btn btn-danger btn-del" data-component="${uuid}"><i class="fa-solid fa-minus"></i></button>`))
        .append(`<select class="form-select flex-grow-1 multi-select${questioncondition}-${designdocumentgroupquestionid}" name="${designdocumentquestionid}" data-questionid="${designdocumentquestionid}" data-componentvalue="${uuid}" ${mandatory1}></select>`))
        .append($(`#btnarea-${designdocumentquestionid}`));

        initialize_multichoice(designdocumentquestionid, uuid, false);
    } else {
        $(`#questiondiv-${designdocumentquestionid}[data-area="${uuidarea}"]`)
        .append($(`<div class="input-group mb-3" data-component="${uuid}" id="btndel-${designdocumentquestionid}">`)
        .append($('<div class="input-group-prepend">').append(`<button type="button" class="btn btn-danger btn-del" data-component="${uuid}"><i class="fa-solid fa-minus"></i></button>`))
        .append(`<select class="form-select flex-grow-1 multi-select${questioncondition}-${designdocumentgroupquestionid}" name="${designdocumentquestionid}" data-questionid="${designdocumentquestionid}" data-componentvalue="${uuid}" ${mandatory1}></select>`))
        .append($(`#btnarea-${designdocumentquestionid}`));
        
        initialize_selectquestion(designdocumentquestionid, questioncondition, uuid, false);
    }
});

$(document).on("click", ".btn-del", function () {
    uuid = $(this).context.attributes["data-component"].value
    $(`[data-component="${uuid}"]`).remove()
});

$(document).on("click", ".btn-next", function () {
    $.LoadingOverlay("show");
    $("input[required]").each(function(){
        if ($(this).val() == "") {
            $.LoadingOverlay("hide");
        }
    });
})