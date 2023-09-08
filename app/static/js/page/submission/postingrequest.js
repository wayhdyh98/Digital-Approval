var contentOrigin = ''
var pemohonnpk = ''

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_contentdocument().then((resolve) => {
        contentOrigin = resolve
        initialize_data();
    })

    console.log(usersess)

    $.LoadingOverlay("hide");
});

async function initialize_contentdocument() {
    return new Promise((resolve, reject) => {
        var url = url_monitoring_viewtracking_designdocument
        var params = {
            'documentid': documentid,
            'activeversion': activeversion
        }
        $.LoadingOverlay("show");

        function success_callback(data) {
            resolve(data.data[0].contentorigin)
        }

        function error_callback() {
            $.LoadingOverlay("hide");
        }

        page.read_data(url, params, 'POST', success_callback, error_callback);
    })
}

async function initialize_data() {
    var url = url_monitoring_viewtracking_bodypart + "/" + $("#requestapprovalid").val()
    function success_callback(data) {
        if (data.data.length > 0 && data.data2.length > 0) {
            set_questionpart(data.data)
            .then(() => {
                question_tables()
                set_table(data.data2)
                .then(() => {
                    var _html = ''
                    reArrangePosition(contentOrigin)
                    _html += replaceTable(contentOrigin)
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
                            $(tr).remove()
                        }
                    })
                })
                $.grid_main("grid-main", data.data2, "requestapprovalauthenticationid", browse_column());

                get_files()
                                
                set_button()
            })
        } else {
            $.LoadingOverlay("hide");
            url = `/submission/submissions/fillformrequest/${$("#requestapprovalid").val()}`
            if (data.data.length > 0 && data.data2.length <= 0) {
                url = `/submission/submissions/authorizationrequest/${$("#requestapprovalid").val()}`
            }

            Swal.fire({
                title: 'Request Approval is Not Completed!',
                text: 'Please complete your request approval first!',
                icon: 'error'
            }).then((result) => {
                /* Read more about isConfirmed */
                if (result.isConfirmed) {
                    window.open(url, '_self')
                }
            })
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

// function ttd_preview(){
//     var url = url_submissions_ttd_preview

//     var params = {
//         'layoutdocument': $("#testimoni").html(),
//         'piclevel': 1,
//         'picsublevel': 1
//     }

//     function success_callback(data) {
//         $("#testimoni").html(data.result)
//     }

//     function error_callback() {
//         $.LoadingOverlay("hide");
//     }

//     page.read_data(url, params, 'POST', success_callback, error_callback);
// }

async function set_questionpart(params) {
    return await new Promise((resolve, reject) => {
        params.forEach((element, index, array) => {
            answer = element.answer
            if (element.questioncondition != 1) {
                answer = element.codevalue
            }
    
            if ($(`#grupquestion-${element.designdocumentgroupquestionid}`).length == 0) {
                $('.question-part')
                .append($(`<div id="grupquestion-${element.designdocumentgroupquestionid}" class="mb-3">`)
                .append(`<h4>${element.grouptitle}</h4>`))
            }
    
            if ($(`[data-questionid="${element.designdocumentquestionid}"]`).length == 0) {
                if (element.questiontype == 0 && element.sectiontype == 0) {
                    $(`#grupquestion-${element.designdocumentgroupquestionid}`)
                    .append($(`<div class="row mb-1" data-questionid="${element.designdocumentquestionid}">`)
                    .append(`<label class="col-sm-2 col-form-label-lg">${element.question}</label>`)
                    .append(`<label class="col-sm-10 col-form-label-lg">${answer}</label>`))
                }
            }

            if (element.questiontype == 1 || element.sectiontype == 1) {
                var groupquestionindex = multirow.findIndex(i => (i.designdocumentgroupquestionid == element.designdocumentgroupquestionid))
                if (groupquestionindex == -1) {
                    multirow.push({
                        designdocumentgroupquestionid: element.designdocumentgroupquestionid,
                        grouptitle: element.grouptitle,
                        designdocumentquestion: [{id: element.designdocumentquestionid, question:element.question, answer: [answer]}]
                    })
                } else {
                    var questionindex = multirow[groupquestionindex]['designdocumentquestion'].findIndex(i => (i.id == element.designdocumentquestionid))
                    if (questionindex == -1) {
                        multirow[groupquestionindex]['designdocumentquestion']
                        .push({id: element.designdocumentquestionid, question:element.question, answer: [answer]})
                    } else {
                        multirow[groupquestionindex]['designdocumentquestion'][questionindex]['answer'].push(answer)
                    }
                }
            }
    
            contentOrigin = contentOrigin.replaceAll(`##Answer_${element.question}##`, answer)
            if (index == array.length-1) resolve()
        })
    })
}

function question_tables() {
    multirow.forEach(item => {
        var table = $("<table style='width: 100%;' border>")
        var thead = $("<thead>")

        var trHead = $("<tr>")
        item.designdocumentquestion.forEach(x => {
            trHead.append(
                $("<th style='border: 1px solid black; padding: 5px;'>").text(x.question)
            )
        })

        trHead.appendTo(thead)
        table.append(thead)
        var tbody = $("<tbody>")
        
        if (item.designdocumentquestion.length != 0) {
            var arranswer = item.designdocumentquestion.map((item, idx, arr) => { return item.answer } )
            var idxhighestarranswer = arranswer.reduce((maxI,el,i,arr) => (el.length>arr[maxI].length) ? i : maxI, 0)
            var transposed_arranswer = arranswer[idxhighestarranswer].map((_, colIndex) => arranswer.map(row => row[colIndex]))

            transposed_arranswer.forEach(answer => {
                var trBody = $("<tr>")
                answer.forEach(x => {
                    trBody.append(
                        $(`<td style="max-width:1px; white-space: normal">`).html(
                            `<span style="word-wrap: break-word; overflow-wrap: break-word">${x}</span>`
                        )
                    )
                })
                trBody.appendTo(tbody)
            })
            table.append(tbody)
        }

        $(`#grupquestion-${item.designdocumentgroupquestionid}`)
        .append(table)
    })
}

function get_files() {
    var url = url_answer_submissions_filerequest + "/" + $("#requestapprovalid").val()

    function success_callback(data) {
        if (data.data.length > 0) {           
            data.data.forEach(element => {
                $(".file-part").append($('<div class="col-md-3">').append(`<a href="${url_download_request_files}/${element.approvalonlinefileid}" for="uploadlampiran" class="form-label mr-2" target="blank"><i class="fa-solid fa-file"></i> ${element.filename}</a>`))
            })
            $.LoadingOverlay("hide");
        } else {
            $(".file-part").append($('<div class="col-md-12 text-center">').append(`<h4><i class="fa-solid fa-file"></i> There's no file in here.</h4>`))
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function set_button(){  
    $('.button-area')
    .append($(`<div class="row mb-1">`)
    .append($('<div class="col-md-3 offset-md-3 text-center">')
    .append(`<button type="button" class="btn btn-danger col-12 btn-cancel my-2" id="btn-cancel" data-color="#dc3545"><i class="fa-solid fa-ban"></i> Cancel</button>`))
    .append($('<div class="col-md-3 text-center">')
    .append(`<button type="button" class="btn btn-success col-12 btn-post my-2" id="btn-post" data-color="#28a745"><i class="fa-solid fa-paper-plane"></i> Submit</button>`)))
}

async function set_table(params){
    var table = $("<table border='1'>")
    table.append(
        $("<tr>")
        .append(
            $("<th>").text("Approver Type"),
            $("<th>").text("Approver Name"),
            $("<th>").text("Approver Status"),
        )
    )

    return await new Promise((resolve, reject) => {
        params.forEach((element, index, array) => {
            ttd = `<img src="/static/whitebg.jpg" width="120px" height="120px" data-authid="${element.requestapprovalauthenticationid}" data-piclevel=${element.piclevel} data-picsublevel=${element.picsublevel} data-ttd="${element.ttd}" data-picid="${element.picid}" data-nosig="${nosig}">`

            if (element["pictype"] == 0) pemohonnpk = element["picid"]
            
            pictype = element["pictype"] == 0 ? "Pemohon" : element["pictype"] == 1 ? "Mengetahui" : "Menyetujui"
            statusapprover = element["statusapprove"] == 0 ? "#ffc107" : element["statusapprove"] == 1 ? "#28a745" : "#dc3545"
            var tr = $("<tr>")
            tr.append(
                $(`<td>${pictype}</td>`),
                $(`<td>${element["picname"]}</td>`),
                $(`<td><span style="
                    background-color: ${statusapprover};
                    border-radius: 0.2rem;
                    color: #fff;
                    display: inline-block;
                    font-size: 80%;
                    font-weight: 500;
                    line-height: 1;
                    padding: 0.3em 0.45em;
                    text-align: center;
                    vertical-align: baseline;
                    white-space: nowrap;">${element["statusapprovetext"]}</span></td>`
                )
            )
            contentOrigin = contentOrigin
                        .replaceAll(`##Authorisasi_${element.piclevel}.${element.picsublevel}##`, ttd)
                        .replaceAll(`##Nama_Authorisasi_${element.piclevel}.${element.picsublevel}##`, element["picname"])
                        .replaceAll(`##Title_Authorisasi_${element.piclevel}.${element.picsublevel}##`, element["descriptionapprovaltitle"])
    
            tr.appendTo(table)
            if (index == array.length-1) {
                $('.tablehtml').append(table)
                resolve()
            }
        })
    })
}

$(document).on("click", ".btn-post", function () {
    var cond = false
    if (pemohonnpk == usersess) {
        cond = true
    }
    url = url_request_submissions_update
    params = {
        'requestapprovalid': $("#requestapprovalid").val(),
        'workflowtable': $(".tablehtml").html(),
        'layoutdocument': $("#testimoni").html(),
        'years': years,
        'cond': cond,
    }

    $.LoadingOverlay("show");
    function success_callback(data) {
        window.open('/submission/submissions', '_self')
        $.LoadingOverlay("hide");
    }
    
    function error_callback() {
        $.LoadingOverlay("hide");
    }
    
    page.read_data(url, params, 'POST', success_callback, error_callback);
    
});

$(document).on("click", ".btn-cancel", function () {
    Swal.fire({
        title: 'Do you want to cancel the request?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: 'Cancel It',
        denyButtonText: `No, I wanna review it again`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            cancel_request()
        } else if (result.isDenied) {
            Swal.fire('Request are not canceled', '', 'info')
        }
    })
});


$(document).on("click", "#btn-preview", function () {
    if (layout == "1") {
        $("#testimoni").css("width", "29.7cm")
        $("#testimoni").css("height", "21cm")
        $(".modal-xl").css("max-width", "1400px")
    } else {
        $("#testimoni").css("height", "29.7cm")
        $("#testimoni").css("width", "21cm")
        $(".modal-xl").css("max-width", "1140px")
    }
    $("#preview-modal").modal("show");
});

function cancel_request(){
    url = url_request_submissions_cancel
    params = {
        'requestapprovalid': $("#requestapprovalid").val(),
    }

    $.LoadingOverlay("show");
    function success_callback(data) {
        window.open('/submission/submissions', '_self')
        $.LoadingOverlay("hide");
    }
    
    function error_callback() {
        $.LoadingOverlay("hide");
    }
    
    page.read_data(url, params, 'POST', success_callback, error_callback);
}

/* define the column of the grid  */
browse_column = function () {
    return [
        {
            dataField: "picid",
            caption: "Approver NPK"
        },
        {
            dataField: "piclevel",
            caption: "Approver Level"
        },
        {
            dataField: "picsublevel",
            caption: "Approver Sub Level"
        },
        {
            dataField: "picname",
            caption: "Approver Name"
        },
        {
            dataField: "descriptionapprovaltitle",
            caption: "Approver Title"
        },
        {
            dataField: "divisi",
            caption: "Approver Division"
        },
        {
            dataField: "commentapprove",
            caption: "Comment"
        },
        {
            dataField: "statusapprovetext",
            caption: "Status Approver"
        },
        {
            dataField: "modifdate",
            caption: "Modif Date",
            dataType: "date",
            format: "yyyy-MM-dd",
            alignment: 'center',
        },
    ];
}