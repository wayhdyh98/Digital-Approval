var requestautharray = []
var picdataarray = []
$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_picdata()

    $.LoadingOverlay("hide");
});

function insert_requestauth(params){
    var url = url_insert_request_auth;

    var params = {
        "requestapprovalid": $("#requestapprovalid").val(),
        "masterapproveid": params["masterapproveid"],
        "pictype": params["pictype"],
        "picid": params["picid"],
        "piclevel": params["piclevel"],
        "picsublevel": params["picsublevel"],
        "picname": params["picname"] ? params["picname"] : "",
        "mandatory": params["mandatory"],
    }

    function success_callback(data) {
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
}

function check_answer() {
    var url = url_answer_submissions_authrequest + "/" + $("#requestapprovalid").val()

    function success_callback(data) {
        if (data.data.length > 0) {
            data.data.forEach(element => {
                $(`[data-authid="${element.masterapproveid}"]`).val(element.picid).change()
            })
            $.LoadingOverlay("hide");
        } else {
            $.LoadingOverlay("hide");
        }
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function initialize_data() {
    var url = url_master_approvals + "/" + $("#documentid").val();

    function success_callback(data) {
        var firstSet = new Promise((resolve, reject) => {
            data.data.forEach((element, index, array) => {
                if (element.picid != "") {
                    insert_requestauth(element)
                } else {
                    requestautharray.push({
                        masterapproveid: element.masterapproveid,
                        picname: element.picname,
                        pictype: element.pictype,
                        picid: element.picid,
                        piclevel: element.piclevel,
                        picsublevel: element.picsublevel,
                        mandatory: element.mandatory
                    })
                }
                
                piclevel = data.data.filter(e => e.piclevel == element.piclevel)
    
                if (piclevel.length > 1) {
                    piclevel = `${element.piclevel}.${element.picsublevel}`
                } else {
                    piclevel = `${element.piclevel}`
                }
                
                pictype = (element.pictype == "0" ? `Pemohon ${piclevel}` : (element.pictype == "1" ? `Mengetahui ${piclevel}` : `Menyetujui ${piclevel}`))
    
                if (element.picid == "" || element.picid == "00000") {
                    // FREE TEXT
                    $("#authform").append($('<div class="auth-side mb-4">').append(`<label class="form-label">${pictype}</label>`).append(`<select class="form-select flex-grow-1 select-auth" name="${element.masterapproveid}" data-authid="${element.masterapproveid}"></select>`))
                    
                    set_picdata(element.masterapproveid)
                } else {
                    // MASTER
                    $("#authform").append($('<div class="auth-side mb-4">').append(`<label class="form-label">${pictype}</label>`).append(`<input type="text" name="${element.masterapproveid}" data-authid="${element.masterapproveid}" disabled readonly class="form-control" value="${element.picid.padStart(5, "0")} - ${element.picname}">`))
                }

                if (index == array.length-1) resolve()
            })
        })
        
        $('[name=arraymasterapproveid]').val(JSON.stringify(requestautharray))

        firstSet.then(() => {
            check_answer()
        })
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function initialize_picdata() {
    var url = `${url_designdocument_questioncondition}/${$("#documentid").val()}/5/2`;

    $.LoadingOverlay("show");
    function success_callback(data) {
        if (data.success == "1") {
            var firstSet = new Promise((resolve, reject) => {
                data.data.forEach((element, index, array) => {
                    picdataarray.push({code: element.code, value: element.value})
                    if (index == array.length-1) resolve()
                });
            })

            firstSet.then(() => {
                initialize_data()
            })
        }
    }
    function error_callback() {
        $.LoadingOverlay("hide");
    }
    
    page.read_data(url, null, 'GET', success_callback, error_callback);
}

function set_picdata(masterapproveid) {
    $(`select[data-authid="${masterapproveid}"]`).children().remove().end();
    picdataarray.forEach(element => {
        $(`select[data-authid="${masterapproveid}"]`).append(`<option value="${element.code}" data-picname="${element.name}">${element.value}</option>`);
    });
    $(`select[data-authid="${masterapproveid}"]`).find( 'option:first' ).prop('selected',true).change()
}

$(document).on("change", ".select-auth", function () {
    masterapproveid = $(this).context.attributes["data-authid"].value

    requestautharray = requestautharray.map(
        element => ({
           masterapproveid: element.masterapproveid,
           picname: element.masterapproveid == masterapproveid ? $(`select[data-authid="${masterapproveid}"] option:selected`).data("picname") : element.picname,
           pictype: element.pictype,
           picid: element.masterapproveid == masterapproveid ? $(`select[data-authid="${masterapproveid}"]`).val() : element.picid,
           piclevel: element.piclevel,
           picsublevel: element.picsublevel,
           mandatory: element.mandatory
        }));
    
    $('[name=arraymasterapproveid]').val(JSON.stringify(requestautharray));
});
