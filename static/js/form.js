$(document).ready(function(){

    $('#submit').click(function(){

        $.ajax({
            headers: { 'X-CSRFToken': csrf_token },
            type: 'POST',
            url: '/web_tool/ajax_data/', 
            data: $('#ajax_form').serialize(),
            success: function(response){ 
                /*抓取 input 列 id = input 的數值*/
                var target = $( "#input" ).val() 
                $('#table1').DataTable({
                    searching: false, 
                    paging: false, 
                    info: false,
                    data: response.data,
                    columns: [
                        { data: 'wormbase_id', title: "Gene ID" },
                        { data: 'gene_sequence', title: "Gene Sequence" },
                        { data: 'numbers', title:"Numbers"},
                        { data: 'gene_name', title: "Gene Name" },
                        { data: 'other_name',title:"Other Name"},
                    ],
                    /*auto refrash*/
                    destroy:true,
                    /*add row colar*/
                    createdRow: function( row, data, ) {
                        if ( data.wormbase_id === target ) {        
                        $(row).addClass('add-background');
                         }
                        else if (data.gene_sequence === target){
                            $(row).addClass('add-background');
                        }
                        else if (data.gene_name === target){
                            $(row).addClass('add-background');
                        }
                        else if (data.other_name === target){
                            $(row).addClass('add-background');
                        }
                    }
                });
                $('#table2').DataTable({
                    searching: false, 
                    paging: false, 
                    info: false,
                    data: response.transcript_and_type,
                    columns: [
                        { data: 'Transcript_ID', title: "Transcript ID",
                        /*add hyperlink*/
                        "render": function (data, type, row, meta)
                        {
                            data = '<a href="/web_tool/table/'+ data +' " target="_blank">' + data + '</a>';
                            return data;
                          }
                    },{data:'Type',title :"Transcript Type"},
                    {
                        data: 'Transcript_ID',
                        title: "pirScan",
                        render: function (data, type, row) {
                            return '<button type="button" onclick="window.open(\'/web_tool/pirscan/' + data + '\', \'_blank\')" class="btn btn-warning btn-sm">site</button>';
                        }
                    },
                    {
                        data: 'Transcript_ID',
                        title: "search",
                        render: function (data, type, row) {
                            return '<button type="button" onclick="window.open(\'/web_tool/search/' + data + '\', \'_blank\')" class="btn btn-info btn-sm">site</button>';
                        }
                    },
                    {
                        data: 'Transcript_ID',
                        title: "22G read count",
                        render: function (data, type, row) {
                            return '<button type="button" onclick="window.open(\'/web_tool/read_count/' + data + '\', \'_blank\')" class="btn btn-danger btn-sm">site</button>';
                        }
                    },
                    ],
                    
                    destroy:true,

                    /*add row colar*/
            
                    createdRow: function( row, data,) {
                        if ( data.Transcript_ID === target ) {        
                        $(row).addClass('add-background');
                        }
                    
                }
                });
            },
            error: function(){
                $("#message").html('<div class="alert alert-warning">' + 'check again !' + '</div>');
                /*alert('Something error');*/
                
            },
        });
    });
});