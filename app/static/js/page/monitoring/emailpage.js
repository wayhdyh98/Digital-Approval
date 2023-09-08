var multirow = []

$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});

function initialize_data() {
    var url = url_monitoring_email_viewtracking_bodypart + "/" + picid + "/" + $("#requestapprovalid").val()
    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.data.length > 0 && data.data2.length > 0) {
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
            })
                            
            set_button(data.key, data.sidedata, data.datapic)
            $.LoadingOverlay("hide");
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
        'requestapprovalid': $("#requestapprovalid").val()
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

            if (index == array.length-1) {
                $('.tablehtml').append(table)
                resolve()
            }
        })
    })
}

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
        var url = url_monitoring_email_viewtracking_approveaction

        var params = {
            'requestapprovalid': $("#requestapprovalid").val(),
            'requestapprovalauthenticationid': authid,
            'commentapprove': text,
            'piclevel': piclevel,
            'picsublevel': picsublevel,
            'picid': picid,
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