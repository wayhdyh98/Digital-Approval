// documents
url_master_documents = "/document/api/1.0/documents";
url_master_documents_divisions = "/document/api/1.0/documentssubmissions";
url_delete_document = "/document/api/1.0/document/delete";

// authorizations
url_master_approvals = "/document/api/1.0/approvals/";
url_insert_approval = "/document/api/1.0/approvals/insert";
url_delete_approval = "/document/api/1.0/approvals/delete";
url_pic_parentapproval = "/document/api/1.0/approval/parent/";

// design documents
url_designdocument_groupquestions = "/document/api/1.0/designdocument/groupquestions/";
url_insert_designdocument_groupquestion = "/document/api/1.0/designdocument/groupquestion/insert";
url_delete_designdocument_groupquestion = "/document/api/1.0/designdocument/groupquestion/delete";
url_designdocument_questions = "/document/api/1.0/designdocument/questions";
url_designdocument_questions_multichoice = "/document/api/1.0/designdocument/questions/multichoice";
url_insert_designdocument_question = "/document/api/1.0/designdocument/question/insert"
url_delete_designdocument_question = "/document/api/1.0/designdocument/question/delete";

// design quill documents
url_designdocument = "/document/api/1.0/designdocument/";
url_insert_designdocument = "/document/api/1.0/designdocument/insert";

// design documents (question condition)
url_designdocument_questioncondition = "/document/api/1.0/designdocument/question/condition/";

// division
url_master_divisions = "/division/api/1.0/divisions";
url_orange_pic_approvals = "/orange/api/1.0/picapprovals";

// clients
url_master_clients = "/client/api/1.0/clients";
url_profile_client = "/client/api/1.0/profile";

// submissions
url_transaction_submissions = "/submission/api/1.0/submissions";
url_answer_submissions_fillformrequest = "/submission/api/1.0/submissions/fillformanswer";
url_answer_submissions_authrequest = "/submission/api/1.0/submissions/authrequest";
url_answer_submissions_filerequest = "/submission/api/1.0/submissions/filerequest";
url_request_submissions_page_1 = "/submission/api/1.0/submissions/requestpage1";
url_request_submissions_update = "/submission/api/1.0/submissions/requestapproval/update";
url_request_submissions_cancel = "/submission/api/1.0/submissions/requestapproval/cancel";
url_insert_request_auth = "/submission/api/1.0/submissions/request_authorization/insert";
url_upload_request_files = "/submission/api/1.0/submissions/request_uploadfile/upload";
url_delete_request_files = "/submission/api/1.0/submissions/request_uploadfile/delete";
url_download_request_files = "/submission/api/1.0/submissions/request_uploadfile/download";
url_submissions_ttd_preview = "/submission/api/1.0/submissions/ttd_preview";
url_request_document = "/submission/api/1.0/submissions/getdocumentrequest"

// monitorings
url_monitoring_documents = "/monitoring/api/1.0/documents";
url_monitoring_viewtracking_designdocument = "/monitoring/api/1.0/viewtracking/designdocument";
url_monitoring_trackingworkflow = "/monitoring/api/1.0/trackingworkflow";
url_monitoring_viewtracking_levelsession = "/monitoring/api/1.0/viewtracking/levelsession"; 
url_monitoring_viewtracking_bodypart = "/monitoring/api/1.0/viewtracking/bodypart";
url_monitoring_email_viewtracking_bodypart = "/monitoring/api/2.0/viewtracking/bodypart";
url_monitoring_viewtracking_approveaction = "/monitoring/api/1.0/viewtracking/approveaction";
url_monitoring_email_viewtracking_approveaction = "/monitoring/api/2.0/viewtracking/approveaction";
url_monitoring_ttd_preview = "/monitoring/api/1.0/viewtracking/ttd_preview";


// profile
url_profile_ttd = "/user/api/1.0/profile/upload";

/** GRID **/

/* create the grid and connect the data */
$.grid_main = function (panel, data, key, browse_column) {
    $('#' + panel).dxDataGrid({
        dataSource: data,
        keyExpr: key,
        selection: {
            mode: 'single',
        },
        hoverStateEnabled: true,
        grouping: {
            autoExpandAll: true,
        },
        groupPanel: {
            visible: true,
        },
        columnAutoWidth: true,
        columns: browse_column,
        showBorders: true,
        filterRow: {
            visible: true,
            applyFilter: 'auto',
        },
        searchPanel: {
            visible: true,
            width: 240,
            placeholder: 'Search...',
        },
        headerFilter: {
            visible: true,
        },
        scrolling: {
            rowRenderingMode: 'virtual',
        },
        paging: {
            pageSize: 20,
        },
        pager: {
            visible: true,
            allowedPageSizes: [10, 20, 50, 'all'],
            showPageSizeSelector: true,
            showInfo: true,
            showNavigationButtons: true,
        },
        export: {
            enabled: true,
            allowExportSelectedData: true,
            fileName: "excel-" + uuidv4()
        },
    });
}

/** FUNCTIONS **/

// division 
function prepare_division(container) {
    var url = url_master_divisions;
    var params = null;

    function success_callback(data) {
        $('#' + container).children().remove().end();
        data.data.forEach(element => {
            $("#" + container).append('<option value='+ element.divisionid +'>'+ element.divisionname +'</option>');
        });
    }

    function error_callback() {
    }

    page.read_data(url, params, 'GET', success_callback, error_callback);
}


// pic approval based on division 
function prepare_approval(container, divisionid) {
    var url = url_orange_pic_approvals + "/" + divisionid;
    var params = null;

    function success_callback(data) {
        $('#' + container).children().remove().end();
        $("#" + container).append('<option value=0></option>');
        data.data.forEach(element => {
            $("#" + container).append('<option value='+ element.employeeid +'>'+ element.displayname +'</option>');
        });
    }

    function error_callback() {
    }

    page.read_data(url, params, 'GET', success_callback, error_callback);
}