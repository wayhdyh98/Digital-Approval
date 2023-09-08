$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    // data grid
    initialize_data();

    $.LoadingOverlay("hide");
});


function initialize_data() {
    var url = url_master_clients;

    function success_callback(data) {
        $.grid_main("grid-main", data.data, "masterdocid", browse_column());
    }

    function error_callback() {
    }

    page.read_data(url, null, 'GET', success_callback, error_callback);
}


/* define the column of the grid  */
browse_column = function () {
    return [
        {
            caption: "#",
            width: 100,
            fixed: true,
            cellTemplate: function (container, info) {
                var $el = $('<div class="row ml-1 mr-1"></div>');
                $('<a class="btn btn-sm btn-dark col-md-12"><i class="fa fa-eye" aria-hidden="true"></i> View</a>')
                    .attr('href', '#')
                    .click(function () {

                        function success_callback(data) {
                            // reset
                            $("#profile-name").text("");
                            $("#position-name").text("");
                            $("#division-name").text("");
                            $("#department-name").text("");
                            $("#company-name").text("");
                            $("#profile-email").attr("href", "#");
                            
                            // fill
                            $("#profile-name").text(data.data.name);
                            $("#position-name").text(data.data.position);
                            $("#division-name").text(data.data.division);
                            $("#department-name").text(data.data.department);
                            $("#company-name").text(data.data.company);
                            $("#profile-email").attr("href", "mailto:" + data.data.email)
                            $('#profile-client-modal').modal("show");
                        }

                        url = url_profile_client + "/" + info.values[1];
                        params = null; 
                        page.read_data(url, params, 'GET', success_callback);
                    }
                    )
                    .appendTo($el);
                container.append($el);
            },
        },
        {
            width: 100,
            fixed: true,
            dataField: "npk",
            caption: "NPK"
        },
        {
            dataField: "name",
            caption: "Name"
        },
        {
            dataField: "email",
            caption: "Email"
        },
    ];
}