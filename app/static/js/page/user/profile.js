$(document).ready(function () {
    console.log("Ready.");

    $.LoadingOverlay("show");

    $.LoadingOverlay("hide");
});


$("#usersession").click(function() {
    icon = $("#userkey").val() != 'None' ? "info" : "question"
    userkey = $("#userkey").val() != 'None' ? $("#userkey").val() : `Sorry, looks like you don't have the key <i class="fa-solid fa-face-sad-tear fa-1x"></i>`
    Swal.fire(
        'User Public Key',
        userkey,
        icon
      )
})

$("a #img-sign").click(async function() {
    const { value: file } = await Swal.fire({
        title: 'Upload signature',
        input: 'file',
        inputAttributes: {
          'accept': 'image/*',
          'aria-label': 'Upload your signature'
        }
    })
      
    if (file) {
    $.LoadingOverlay("show");
    var url = url_profile_ttd;
    var img = ''
    var reader = new FileReader()
    reader.onload = (e) => {
        img = e.target.result
    }
    reader.readAsDataURL(file)

    setTimeout(() => {
        params = {
            "file": img
        }

        function success_callback(data) {
            if (data.success == "1") {
                $("#img-sign").attr("src", img)
                $.LoadingOverlay("hide");
            }
            else {
                Swal.fire(data.message, '', 'error');
                $.LoadingOverlay("hide");
            }
            $(this).val(null);
        }

        function error_callback() {
            $.LoadingOverlay("hide");
        }

        page.read_data(url, params, 'POST', success_callback, error_callback);
    }, 500)
    }
})
