$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    if (validation_insert == "True") {
        Swal.fire({
            title: `Document with the same version has been created!`,
            icon: 'error'
        })
    }

    $.LoadingOverlay("hide");
});

$('#documentversion').keypress(function (e) {    
    var charCode = (e.which) ? e.which : event.keyCode    
    if (String.fromCharCode(charCode).match(/[^0-9]/g))    
        return false
    if (this.value.length == 0 && charCode == 48 )
        return false
    if (this.value.length == 5)
        return false
});

$('#documentversion').attr("min", "1");