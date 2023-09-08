$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    prepare_form_filter();

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});


function prepare_form_filter() {
}


function initialize_data() {
    var data = {
        "requestapprovalid": "",
        "name": "",
        "desc": "",
        "createddate": "",
    }
    $.grid_main("grid-main", data, "requestapprovalid", browse_column());
}


$(document).on("click", ".btn-filter", function () {
    var status = $("#select-status-approval").val();
    var url = url_transaction_submissions + "/" + status;

    $.LoadingOverlay("show");
    function success_callback(data) {
        $.grid_main("grid-main", data.data, "requestapprovalid", browse_column());
        $.LoadingOverlay("hide");
    }

    function error_callback() {
        $.LoadingOverlay("hide");
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
});


/* define the column of the grid  */
browse_column = function () {
    return [
        {
            caption: "#",
            width: 300,
            fixed: true,
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                if (info.data.statusrequest == 0) {
                    $('<a class="btn btn-sm btn-warning col-md-3"><i class="fa fa-pen" aria-hidden="true"></i> Edit</a>')
                    .attr('href', '/submission/submissions/fillformrequest/' + info.data.requestapprovalid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);
                    $('<a class="btn btn-sm btn-dark col-md-3"><i class="fa fa-eye" aria-hidden="true"></i> View</a>')
                    .attr('href', '/submission/submissions/postingrequest/' + info.data.requestapprovalid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);
                container.append($el);
                } else if (info.data.statusrequest == 1) {
                    $('<a class="btn btn-sm btn-dark col-md-3"><i class="fa fa-eye" aria-hidden="true"></i> View</a>')
                    .attr('href', '/monitoring/trackingworkflow/view/' + info.data.requestapprovalid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);
                container.append($el);
                }
            },
        },
        {
            dataField: "requestid",
            caption: "Request Id"
        },
        {
            dataField: "name",
            caption: "Document Name"
        },
        {
            dataField: "desc",
            caption: "Notes"
        },
        {
            dataField: "createddate",
            caption: "Created Date",
            dataType: "date",
            format: "yyyy-MM-dd",
            alignment: 'center',
        },
    ];
}