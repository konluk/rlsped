
$(document).ready(function(){

    $("#add-transport").click(function(){
        req_data = {
            client_id: $("#client_id").val(),
            zip_from: $("#zip_from").val(),
            zip_to: $("#zip_to").val()
        }
        console.log(req_data)
        $.ajax({
            url: "/api/addTransport",
            type: "POST",
            data: req_data,
            success: function(response){
                console.log("Success:", response);
                reloadTransports();
                $("#client_id").val("");
                $("#zip_from").val("");
                $("#zip_to").val("");
            },
            error: function(xhr, textStatus, errorThrown){
                console.log("Error:", xhr.responseText);
                alert(xhr.responseText)
            }
        });
    });

    $(document).on('click', '.delete-transport', function() {
        $.ajax({
            url: "/api/deleteTransport",
            type: "POST",
            data: {
                transport_id:$(this).attr("rowid")
            },
            success: function(response){
                console.log("Success:", response);
                reloadTransports();
            },
            error: function(xhr, textStatus, errorThrown){
                console.log("Error:", xhr.responseText);
                alert(xhr.responseText)
            }
        });
    });

    function reloadTransports(){
        $('#transports-table-body').empty();
        $.ajax({
            url: '/api/getTransports',
            type: 'GET',
            success: function(data) {
                $.each(data, function(index, trans) {
                    removeButton = '<button type="button" class="btn btn-dark mx-3 delete-transport" rowid="'+trans.id+'" style="font-size:10px;">X</button>'

                    var row = '<tr>' +
                              '<td>' + trans.id + '</td>' +
                              '<td>' + trans.client_id + '</td>' +
                              '<td>' + trans.info_from + '</td>' +
                              '<td>' + trans.info_to + '</td>' +
                              '<td>' + trans.created_date + '</td>' +
                              '<td>' + removeButton + '</td>' +
                              '</tr>';
                    $('#transports-table-body').append(row);
                });

            },
            error: function(xhr, status, error) {
                console.error('Error occurred:', error);
            }
        });
    }

    reloadTransports();
});