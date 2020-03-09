$(document).ready(function () {
    $('#id_techop').change(function() {
        // this will contain a reference to the checkbox   
        if (this.checked) {
            console.log("checked");
            $('#id_seton').prop('checked', false);
            $('#id_seton').attr("disabled", true);
            // the checkbox is now checked 
        } else {
            $('#id_seton').removeAttr("disabled");
            console.log("unchecked");
            // the checkbox is now no longer checked
        }
    });
});