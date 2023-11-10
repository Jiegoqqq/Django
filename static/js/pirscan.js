
$(document).ready(function(){
    const $loadingSpinner = $('#loading-spinner');
    const $loadingContainer = $('#loading-container');
    $loadingSpinner.show();
    $loadingContainer.show();
    var URL = document.URL; //用這個可以得到現在的URL網址
    transcript = URL.replace('http://127.0.0.1:8000/web_tool/pirscan/',''); //得到transcript id

    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        url: '/web_tool/pirScan_data/', 
        data: {'transcript_id':transcript},
 
        success: function(response){
            pirScan_d3_line=response.pirScan_d3_line
//for spliced d3 line & tooltips
            const svg_p = d3.select("#pirScan_d3");
            const tooltip_p = d3.select(".tooltip_p");
            //to match the line with the svg width
            const svgWidth_p = +svg_p.attr("width");
            const maxX2_p = d3.max(pirScan_d3_line, d => d.x2);

            // Create an xScale based on the maximum x2 value
            const xScale_p = d3.scaleLinear()
              .domain([0, maxX2_p])
              .range([0, svgWidth_p]);


            function showTooltip_p(d) {
                tooltip_p.style("opacity", 1) // 顯示tooltips
                tooltip_p.html(`Type:${d.target.__data__.Type}<br>Start:${d.target.__data__.start}<br>End:${d.target.__data__.end}`); //呈現文字在html 用 target.__data__ 找
              }
              
            function hideTooltip_p() { tooltip_p.style("opacity", 0); }
            svg_p.selectAll("line")
            .data(pirScan_d3_line)
            .enter().append("line")
            .attr("x1", d => xScale_p(d.x1))
            .attr("y1", d => d.y1)
            .attr("x2", d => xScale_p(d.x2))
            .attr("y2", d => d.y2)
            .attr("stroke", d => d.color)
            .attr("stroke-width", 10)
            .attr("fill", "none")
            
            .on("mouseover",showTooltip_p) // Show tooltip on mouseover
            .on("mousemove", (d) => {
                tooltip_p
                .style('left', d.pageX+'px') // 設定tooltips位置
                .style('top', d.pageY+'px')
            })
            .on("mouseout", hideTooltip_p); // Hide tooltip on mouseout

                        //add scale axis
            var scale_p = d3.scaleLinear()
                            .domain([0,maxX2_p])
                            .range([10,1800]);
            const xAxis_p = d3.axisBottom(scale_p);

            // Append a group element to the SVG to hold the axis
            svg_p.append("g")
            .attr("class", "x-axis") // You can add a class for styling
            .attr("transform", `translate(0, ${165})`) // Adjust the y position as needed
            .call(xAxis_p);
            
            // Style the axis ticks and text
            svg_p.selectAll(".x-axis text")
            .style("text-anchor", "middle") // Adjust text alignment as needed
            .attr("dy", "1em"); // Adjust the vertical position of the text

// for DataTable
            $('#table1').DataTable({
                searching: false, 
                paging: false, 
                info: false,
                ordering: false,
                data: response.table_dict,

                
                columns: [
                    { data: 'piRNA', title: "piRNA" },
                    { data: 'piRNA_target_score', title: "piRNA_target_score" },
                    { data: 'mismatches', title: "mismatches"},
                    { data: 'target_region', title: "target region" },
                    { data: 'position_in_piRNA', title: "position in piRNA" },
                    { data: 'non_GU_mismatches_in_seed_region',title:"non-GU mismatches in seed region"},
                    { data: 'GU_mismatches_in_seed_region',title:"GU mismatches in seed region"},
                    { data: 'non_GU_mismatches_in_non_seed_region',title:"non-GU mismatches in non seed region"},
                    { data: 'Gu_mismatches_in_non_seed_region',title:"Gu mismatches in non seed region"},
                    { data: 'pairing (top:Input sequence, bottom:piRNA)', title: "pairing (top:Input sequence, bottom:piRNA)"},
                    { data: 'start', title: "start"},
                    { data: 'end', title: "end"},
                ],
    
                destroy:true,
            });
            $loadingSpinner.hide();
            $loadingContainer.hide();
        },
        error: function(){
            $loadingSpinner.hide();
            $loadingContainer.hide();
            alert('Something error');
            
            
        },
    });
});