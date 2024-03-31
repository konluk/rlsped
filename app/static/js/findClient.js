
$(document).ready(function(){
    $("#search-zip-btn").click(function(){
        $('#search-table-body').empty();
        req_data = {
            searchzip: $("#search_zip").val()
        }
        $.ajax({
            url: "/api/findClients",
            type: "POST",
            data: req_data,
            success: function(data){
                console.log(data);
                console.log(data.clients);
                $.each(data.clients, function(index, trans) {
                    var row = '<tr>' +
                                  '<td>' + trans.distance + ' KM</td>' +
                                  '<td>' + trans.client_id + '</td>' +
                                  '<td>' + trans.info_from + '</td>' +
                                  '<td>' + trans.info_to + '</td>' +
                                  '<td><input class="form-check-input" type="checkbox"></td>' +
                               '</tr>';
                    $('#search-table-body').append(row);
                });
            },
            error: function(xhr, textStatus, errorThrown){
                console.log("Error:", xhr.responseText);
                alert(xhr.responseText)
            }
        });
    });
});