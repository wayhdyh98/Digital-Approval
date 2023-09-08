$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});


function initialize_data() {
    var url = url_master_documents;

    function success_callback(data) {
        $.grid_main("grid-main", data.data, "masterdocid", browse_column());
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}


function delete_document(documentid) {
    var url = url_delete_document;
    var params = {
        "documentid": documentid
    }

    function success_callback(data) {
        if (data.success == '1') {
            Swal.fire('Delete!', '', 'success').then(function () {
                initialize_data();
            });
        }
    }

    function error_callback() {
    }

    page.read_data(url, params, 'POST', success_callback, error_callback);
}


/* define the column of the grid  */
browse_column = function () {
    return [
        {
            caption: "#",
            width: 300,
            fixed: true,
            headerCellTemplate: function (header, info) {
                $('<a>New</a>')
                    .attr('href', '/document/add')
                    .attr('title', 'New Master Dokumen')
                    .appendTo(header);
            },
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                $('<a class="btn btn-sm btn-dark col-md-3"><i class="fa fa-pen" aria-hidden="true"></i> Edit</a>')
                    .attr('href', '/document/edit/' + info.data.masterdocid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);
                $('<a class="btn btn-sm btn-danger col-md-3"><i class="fa fa-trash" aria-hidden="true"></i> Delete</a>')
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
                                delete_document(info.data.masterdocid);
                            } else if (result.isDenied) {
                                Swal.fire('Data are not deleted', '', 'info')
                            }
                        })
                    }
                    )
                    .appendTo($el);
                $('<a class="btn btn-sm btn-warning col-md-3"><i class="fa fa-key" aria-hidden="true"></i> Auth</a>')
                    .attr('href', '/document/authorization/' + info.data.masterdocid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);
                $('<a class="btn btn-sm btn-success col-md-3"><i class="fa fa-pen-fancy" aria-hidden="true"></i> Design</a>')
                    .attr('href', '/document/design/' + info.data.masterdocid)
                    .click(function () {
                    }
                    )
                    .appendTo($el);

                container.append($el);
            },
        },
        {
            dataField: "name",
            caption: "Name"
        },
        {
            dataField: "version",
            caption: "Version",
            alignment: 'center',
        },
        {
            dataField: "isprint",
            caption: "Print",
            alignment: 'center',
            cellTemplate: function (container, options) {
                if (options.value == "1") {
                    $('<span>Dicetak</span>').appendTo(container);
                }
                else if (options.value == "0") {
                    $('<span>Tidak Dicetak</span>').appendTo(container);
                }
            },
        },
        {
            dataField: "status",
            caption: "Is Active?",
            alignment: 'center',
            cellTemplate: function (container, options) {
                if (options.value == "1") {
                    $('<h6><span class="badge badge-success col">Active</span></h6>').appendTo(container);
                }
                else if (options.value == "0") {
                    $('<h6><span class="badge badge-danger col">In-active</span></h6>').appendTo(container);
                }
            },
        },
        {
            dataField: "createddate",
            caption: "Created Date",
            dataType: "date",
            format: "yyyy-MM-dd",
            alignment: 'center',
        },
        {
            dataField: "desc",
            caption: "Notes"
        },
    ];
}