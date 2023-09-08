var multirow = []
var lockprint = false

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});

function initialize_data() {
    var url = url_monitoring_viewtracking_bodypart + "/" + $("#requestapprovalid").val()
    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.data.length > 0 && data.data2.length > 0) {
            set_questionpart(data.data)
            .then(() => {
                question_tables()
                set_table(data.data2)
                .then(() => {
                    if (layout == "1") {
                        $("#testimoni").css("width", "29.7cm")
                        $("#testimoni").css("height", "21cm")
                        $(".modal-xl").css("max-width", "1400px")
                    } else {
                        $("#testimoni").css("height", "29.7cm")
                        $("#testimoni").css("width", "21cm")
                        $(".modal-xl").css("max-width", "1140px")
                    }

                    $('#btn-print').prop("disabled", lockprint)
                    console.log("done")
                })
                $.grid_main("grid-main", data.data2, "requestapprovalauthenticationid", browse_column());

                get_files()
                                
                set_button(data.key, data.sidedata, data.datapic)
            })
        } else {
            $.LoadingOverlay("hide");
            Swal.fire({
                title: 'Request Approval is Not Completed!',
                text: 'Please complete your request approval first!',
                icon: 'error'
            }).then((result) => {
                /* Read more about isConfirmed */
                if (result.isConfirmed) {
                    window.open(`/submission/submissions/fillformrequest/${$("#requestapprovalid").val()}`, '_self')
                }
            })
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

$(document).on("click", "#btn-preview", function () {
    $.LoadingOverlay("show");
    var url = url_monitoring_ttd_preview

    var params = {
        'layoutdocument': $("#testimoni").html(),
        'requestapprovalid': $("#requestapprovalid").val(),
        'masterdocid': masterdoc
    }

    function success_callback(data) {
        $("#testimoni").html(data.result)
        $("#preview-modal").modal('show')
        $.LoadingOverlay("hide");
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
})

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
                $("<th style='border: 1px solid black; padding: 5px'>").text(x.question)
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

function set_button(params, sidedata){  
    if (params) {
        $('.button-area')
        .append($(`<div class="row mb-1">`)
        .append($('<div class="col-md-3 offset-md-3 text-center">')
        .append(`<button type="button" class="btn btn-danger col-12 btn-action my-2" data-authid="${sidedata.requestapprovalauthenticationid}" data-piclevel="${sidedata.piclevel}" data-picsublevel="${sidedata.picsublevel}" data-btn="Rejected" data-color="#dc3545"><i class="fa-solid fa-thumbs-down"></i> Reject</button>`))
        .append($('<div class="col-md-3 text-center">')
        .append(`<button type="button" class="btn btn-success col-12 btn-action my-2" data-authid="${sidedata.requestapprovalauthenticationid}" data-piclevel="${sidedata.piclevel}" data-picsublevel="${sidedata.picsublevel}" data-btn="Approved" data-color="#28a745"><i class="fa-solid fa-thumbs-up"></i> Approve</button>`)))
    }
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
    
            tr.appendTo(table)
            if (element["statusapprove"] == 2) {
                lockprint = true
            }

            if (index == array.length-1) {
                $('.tablehtml').append(table)
                resolve()
            }
        })
    })
}

$(document).on("click", "#btn-print", function () {
    var printContents = $('#testimoni').html()
    var winPrint = window.open('', '', 'left=0,top=0,width=800,height=600,toolbar=0,scrollbars=0,status=0');
    winPrint.document.write(printContents);
    winPrint.document.close();
    winPrint.focus();
    setTimeout(() => { winPrint.print(); winPrint.close(); }, 1000) 
})

$(document).on("click", ".btn-action", async function () {
    var button = $(this).context.attributes["data-btn"].value
    var color = $(this).context.attributes["data-color"].value
    var authid = $(this).context.attributes["data-authid"].value
    var piclevel = $(this).context.attributes["data-piclevel"].value
    var picsublevel = $(this).context.attributes["data-picsublevel"].value

    var { value: text } = await Swal.fire({
        input: 'textarea',
        inputLabel: `Why you ${button} this request?`,
        inputPlaceholder: 'Type your comment here...',
        inputAttributes: {
          'aria-label': 'Type your comment here'
        },
        inputValidator: (value) => {
            if (!value) {
              return 'You need to write something!'
            }
        },
        showCancelButton: true
    })
      
    if (text) {
        $.LoadingOverlay("show");
        var url = url_monitoring_viewtracking_approveaction

        var params = {
            'requestapprovalid': $("#requestapprovalid").val(),
            'requestapprovalauthenticationid': authid,
            'commentapprove': text,
            'piclevel': piclevel,
            'picsublevel': picsublevel,
            'statusapprove': 0,
            'textstatus': button,
            'colorstatus': color,
            'masterdocid': masterdoc,
            'workflowtable': $(".tablehtml").html(),
            'layoutdocument': $("#testimoni").html()
        }

        params["statusapprove"] = (button == "Approved" ? 1 : 2)

        function success_callback(data) {
            window.open('/monitoring/trackingworkflow', '_self')
            $.LoadingOverlay("hide");
        }
    
        function error_callback() {
            $.LoadingOverlay("hide");
        }
    
        page.read_data(url, params, 'POST', success_callback, error_callback);
    }
})

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
            dataField: "divisi",
            caption: "Approver Division"
        },
        {
            dataField: "commentapprove",
            caption: "Comment"
        },
        {
            dataField: "statusapprovetext",
            caption: "Status Approver",
            cellTemplate: function (container, options) {
                if (options.value == "Approved") {
                    $(`<h6><span class="badge badge-success col">${options.value}</span></h6>`).appendTo(container);
                }
                else if (options.value == "Rejected") {
                    $(`<h6><span class="badge badge-danger col">${options.value}</span></h6>`).appendTo(container);
                } else {
                    $(`<h6><span class="badge badge-warning col">${options.value}</span></h6>`).appendTo(container);
                }
            },
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