$(document).ready(function(){
    //for loading Spinners
    const $loadingSpinner = $('#loading-spinner');
    const $loadingContainer = $('#loading-container');
    $loadingSpinner.show();
    $loadingContainer.show();

    //for hide element
    $("#table1").hide();
    $("#table2").hide();
    $("#table3").hide();
    $("#unspliced_title").hide();
    $("#unspliced_sequence").hide();
    $("#spliced_title").hide();
    $("#spliced_sequence").hide();
    $("#protein_title").hide();
    $("#protein_sequence").hide();
    $("#tag_legend").hide();
    $("#tag_exon_1").hide();
    $("#tag_exon_2").hide();
    $("#tag_UTR").hide();
    $("#tag_intron").hide();
    $("#tag_legend_s").hide();
    $("#tag_exon_1_s").hide();
    $("#tag_exon_2_s").hide();
    $("#tag_UTR_s").hide();
    $("#unspliced_d3").hide();
    $("#spliced_d3").hide();



    $("#toggleBtn1").on('click', function(){
        $("#unspliced_title").toggle("slow");
        $("#table1").toggle("slow");
        $("#unspliced_sequence").toggle("slow");
        $("#tag_legend").toggle("slow");
        $("#tag_exon_1").toggle("slow");
        $("#tag_exon_2").toggle("slow");
        $("#tag_UTR").toggle("slow");
        $("#tag_intron").toggle("slow");
        $("#unspliced_d3").toggle("slow");
    });
    $("#toggleBtn2").on('click', function(){
        $("#spliced_title").toggle("slow");
        $("#table2").toggle("slow");
        $("#spliced_sequence").toggle("slow");
        $("#tag_legend_s").toggle("slow");
        $("#tag_exon_1_s").toggle("slow");
        $("#tag_exon_2_s").toggle("slow");
        $("#tag_UTR_s").toggle("slow");
        $("#spliced_d3").toggle("slow");
    });
    $("#toggleBtn3").on('click', function(){
        $("#protein_title").toggle("slow");
        // $("#table3").toggle("slow");
        $("#protein_sequence").toggle("slow");
    });


    
    var URL = document.URL; //用這個可以得到現在的URL網址
    transcript = URL.replace('http://127.0.0.1:8000/web_tool/table/',''); //得到transcript id
    //變數要用dict的方法傳且經由csrf_token

    

    $("#message").html('<div class="alert alert-warning">' + 'data loading....' + '</div>')

    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        url: '/web_tool/transcript/', 
        data: {'transcript_id':transcript},
 
        success: function(response){

            
            //for title
            unspliced_title = response.unspliced_title
            spliced_title = response.spliced_title
            protein_title = response.protein_title
            //for sequence
            unspliced_sequence = response.unspliced_sequence //unspliced 序列
            spliced_sequence = response.spliced_sequence //spliced 序列
            protein_sequence = response.protein_sequence //protein 序列
            //for table colar
            unspliced_index=response.unspliced_index
            splice_index=response.spliced_index
            //for d3
            unspliced_d3_line=response.unspliced_d3_line
            spliced_d3_line=response.spliced_d3_line
            //for table 
            translation_list=response.translation

            //unspliced sequence
                // set numbers
            for (let i=0;i<unspliced_title.length;i++){
                $("#unspliced_title").append(`<span class='number_title'>${unspliced_title[i]}</span><br>`)
                }; 
                //set sequence 
            let unspliced_color=''
            let color_type_u =''
            for (let i=0; i<unspliced_sequence.length;i++){
                if(unspliced_index[i] == 1){
                    color_type_u = 'five_utr_sequence'
                }else if (unspliced_index[i] == 2){
                    color_type_u = 'exon_sequence_0'
                }else if (unspliced_index[i] == 3){
                    color_type_u = 'exon_sequence_1'
                }else if (unspliced_index[i] == 4){
                    color_type_u ='intron_sequence'
                }else if (unspliced_index[i] == 5){
                    color_type_u ='three_utr_sequence'
                }
                unspliced_color += '<span class='+ color_type_u + '>' +unspliced_sequence[i] + '</span>'
            }
            $("#unspliced_sequence").append(unspliced_color)
            //for d3 line & tooltips
            
            const svg_u = d3.select("#unspliced_d3");
            const tooltip_u = d3.select(".tooltip_u");
            //to match the line with the svg width
            const svgWidth_u = +svg_u.attr("width");
            

            // Calculate the maximum and minimum x2 values from your data
            const maxX2_u = d3.max(unspliced_d3_line, (d) => d.x2);
            const minX2_u = d3.min(unspliced_d3_line, (d) => d.x1);
            // Create an xScale based on the maximum x2 value
            const xScale_u = d3.scaleLinear()
              .domain([minX2_u, maxX2_u])
              .range([0, svgWidth_u]);


            function showTooltip_u(d) {
                tooltip_u.style("opacity", 1) // 顯示tooltips
                tooltip_u.html(`Type:${d.target.__data__.Type}<br>Start:${d.target.__data__.start}<br>End:${d.target.__data__.end}`); //呈現文字在html 用 target.__data__ 找
              }
              
            function hideTooltip_u() { tooltip_u.style("opacity", 0); }
            svg_u.selectAll("line")
            .data(unspliced_d3_line)
            .enter().append("line")
            .attr("x1", d => xScale_u(d.x1))
            .attr("y1", d => d.y1)
            .attr("x2", d => xScale_u(d.x2))
            .attr("y2", d => d.y2)
            .attr("stroke", d => d.color)
            .attr("stroke-width", 10)
            .attr("fill", "none")
            
            .on("mouseover",showTooltip_u) // Show tooltip on mouseover
            .on("mousemove", (d) => {
                tooltip_u
                .style('left', d.pageX+'px') // 設定tooltips位置
                .style('top', d.pageY+'px')
            })
            .on("mouseout", hideTooltip_u); // Hide tooltip on mouseout

            //add scale axis
            var scale_u = d3.scaleLinear()
                            .domain([0,maxX2_u])
                            .range([10,1800]);
            const xAxis_u = d3.axisBottom(scale_u);

            // Append a group element to the SVG to hold the axis
            svg_u.append("g")
            .attr("class", "x-axis") // You can add a class for styling
            .attr("transform", `translate(0, ${80})`) // Adjust the y position as needed
            .call(xAxis_u);
            
            // Style the axis ticks and text
            svg_u.selectAll(".x-axis text")
            .style("text-anchor", "middle") // Adjust text alignment as needed
            .attr("dy", "1em"); // Adjust the vertical position of the text
       

            //spliced sequence
                // set numbers
            for (var i=0;i<spliced_title.length;i++){
                $("#spliced_title").append(`<span class='number_title'>${unspliced_title[i]}</span><br>`)
                 }; 
                // set sequence
            let spliced_color=''
            let color_type_s=''
            for (let i=0; i<spliced_sequence.length;i++){
                if(splice_index[i] == 1){
                    color_type_s = 'five_utr_sequence'
                }else if (splice_index[i] == 2){
                    color_type_s = 'exon_sequence_0'
                }else if (splice_index[i] == 3){
                    color_type_s = 'exon_sequence_1'
                }else if (splice_index[i] == 5){
                    color_type_s ='three_utr_sequence'
                }
                spliced_color += '<span class='+ color_type_s + '>' +spliced_sequence[i] + '</span>'
            }
            $("#spliced_sequence").append(spliced_color)

            //for d3 line & tooltips
            
            const svg_s = d3.select("#spliced_d3");
            const tooltip_s = d3.select(".tooltip_s");
            //to match the line with the svg width
            const svgWidth_s = +svg_s.attr("width");
            const maxX2_s = d3.max(spliced_d3_line, d => d.x2);

            // Create an xScale based on the maximum x2 value
            const xScale_s = d3.scaleLinear()
              .domain([0, maxX2_s])
              .range([0, svgWidth_s]);

            function showTooltip_s(d) {
                tooltip_s.style("opacity", 1) // 顯示tooltips
                tooltip_s.html(`Type:${d.target.__data__.Type}<br>Start:${d.target.__data__.start}<br>End:${d.target.__data__.end}`); //呈現文字在html 用 target.__data__ 找
              }
              
            function hideTooltip_s() { tooltip_s.style("opacity", 0); }
            svg_s.selectAll("line")
            .data(spliced_d3_line)
            .enter().append("line")
            .attr("x1", d => xScale_s(d.x1))
            .attr("y1", d => d.y1)
            .attr("x2", d => xScale_s(d.x2))
            .attr("y2", d => d.y2)
            .attr("stroke", d => d.color)
            .attr("stroke-width", 10)
            .attr("fill", "none")
            .on("mouseover",showTooltip_s) // Show tooltip on mouseover
            .on("mousemove", (d) => {
                tooltip_s
                .style('left', d.pageX+'px') // 設定tooltips位置
                .style('top', d.pageY+'px')
            })
            .on("mouseout", hideTooltip_s); // Hide tooltip on mouseout
            
            //add scale axis
            var scale_s = d3.scaleLinear()
                            .domain([0,maxX2_s])
                            .range([10,1800]);
            const xAxis_s = d3.axisBottom(scale_s);

            // Append a group element to the SVG to hold the axis
            svg_s.append("g")
            .attr("class", "x-axis") // You can add a class for styling
            .attr("transform", `translate(0, ${80})`) // Adjust the y position as needed
            .call(xAxis_s);
            
            // Style the axis ticks and text
            svg_s.selectAll(".x-axis text")
            .style("text-anchor", "middle") // Adjust text alignment as needed
            .attr("dy", "1em"); // Adjust the vertical position of the text

            //proteim sequence
            if (translation_list[0] == 'stop') {
                // Remove the elements with IDs "protein_title" and "protein_sequence"
                $("#protein_title, #protein_sequence, #toggleBtn3").remove();
            }
            else {
                    // set numbers
                for (var i=0;i<protein_title.length;i++){
                    $("#protein_title").append(`<span class='number_title'>${unspliced_title[i]}</span><br>`)
                }; 
                    // set sequence
                for (var i=0;i<protein_sequence.length;i++){
                    $("#protein_sequence").append(`<span class='protein_sequence'>${protein_sequence[i]}</span>`)
                };
            }

            
            $('#table1').DataTable({
                searching: false, 
                paging: false, 
                info: false,
                ordering: false,
                data: response.unspliced_table,
                
                columns: [
                    { data: 'Name', title: "Name" },
                    { data: 'Start', title: "Start" },
                    { data: 'End', title: "End" },
                    { data: 'Length',title:"Length"},
                ],
    
                destroy:true,
            });
            $('#table2').DataTable({
                searching: false, 
                paging: false, 
                info: false,
                ordering: false,
                data: response.spliced_table,
                
                columns: [
                    { data: 'Name', title: "Name" },
                    { data: 'Start', title: "Start" },
                    { data: 'End', title: "End" },
                    { data: 'Length',title:"Length"},
                ],
    
                destroy:true,
            });
            // $('#table3').DataTable({
            //     searching: false, 
            //     paging: false, 
            //     info: false,
            //     ordering: false,
            //     data: response.translation,
                
            //     columns: [
            //         { data: 'translation', title: "Protein" },
            //     ],
    
            //     destroy:true,
            // });


        //for loading Spinners
            $loadingSpinner.hide();
            $loadingContainer.hide();
            $("#message").html('<div class="alert alert-warning">' + 'data ready !' + '</div>');
        },
        error: function(){
            alert('Something error');
        //for loading Spinners
            $loadingSpinner.hide();
            $loadingContainer.hide();
        },
        
    });
});