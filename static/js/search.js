$(document).ready(function(){
    //$("#tag1").hide();
    var URL = document.URL; //用這個可以得到現在的URL網址
    transcript = URL.replace('http://127.0.0.1:8000/web_tool/search/',''); //得到transcript id
    //event.preventDefault();
    let tag =`            
            <div class="card-body">
            <div class="hint d-flex justify-content-end">
                <span class="GU">&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <span>:G-U Mismatch&nbsp;</span>
                <span class="NGU">&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <span>:non G-U Mismatch&nbsp;</span>
                <span class="BULGE">&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <span>:Bulge&nbsp;</span>
                <span class="MUTATION-FONT">T</span>
                <span>:Mutation&nbsp;</span>
                <span>ss</span>
            </div>
            <table class="table table-striped" id="table1" ></table><br> 
            </div>
        <div class="hint d-flex justify-content-end mb-2" id="graphical_view_hint">
                        
            <span class="UTR5">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>5'UTR&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="CDS">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>CDS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="UTR3">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>3'UTR&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="IDREGION">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>CLASH identified region&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="MUTATION">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>Reads with mutation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="GU">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>G-U Mismatch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="NGU">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>non G-U Mismatch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span class="BULGE">&nbsp;&nbsp;&nbsp;&nbsp;</span>
            <span>Bulge&nbsp;</span>
        </div>
        <div class="tooltip" style="opacity: 0;"></div>
        <svg width="1250" height="150" id="search_d3"></svg>

        
        <div class="tooltip_c" style="opacity: 0;"></div>
        <svg width="1250" height="300" id="clash_d3"></svg>

        </div>
        `;
        document.getElementById('tag1').innerHTML = tag;

    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        url: '/web_tool/search_data/', 
        data: {'transcript_id':transcript,},
 
         success: function(response){
            select_list=response.select_list


            let target_table = '<thead> <tr> <th><input type="checkbox" id="select_all" onclick="toggleAll(this)"> Select all<br></th></tr> </thead> <tbody>'
            for (let i = 0; i < select_list.length; i++) {
                target_table += '<tr> &nbsp; &nbsp;&nbsp;<input type="checkbox" class="miRNA-checkbox" id="' + select_list[i] + '_selection" name="foo"> <label for="' + select_list[i] + '_selection"> &nbsp;:&nbsp;' + select_list[i] + '</label><br> <tr>';
            }
            target_table += '</tbody>'
            // Append the generated HTML to the target_table
            document.getElementById('target_table').innerHTML = target_table;
            //let first checkbox to be click default
            const firstCheckbox = document.querySelector('.miRNA-checkbox');
            firstCheckbox.checked = true;

    //for d3
        search_d3_line=response.search_d3_line
        clash_d3_line=response.clash_d3_line

        //for spliced d3 line & tooltips (spliced)
        const svg = d3.select("#search_d3");
        const tooltip = d3.select(".tooltip");
        //to match the line with the svg width
        const svgWidth = +svg.attr("width");
        const maxX2 = d3.max(search_d3_line, d => d.x2);

        // Create an xScale based on the maximum x2 value
        const xScale = d3.scaleLinear()
            .domain([0, maxX2])
            .range([0, svgWidth]);


        function showTooltip(d) {
            tooltip.style("opacity", 1) // 顯示tooltips
            tooltip.html(`Type:${d.target.__data__.Type}<br>Start:${d.target.__data__.start}<br>End:${d.target.__data__.end}`); //呈現文字在html 用 target.__data__ 找
            }
            
        function hideTooltip() { tooltip.style("opacity", 0); }
        svg.selectAll("line")
        .data(search_d3_line)
        .enter().append("line")
        .attr("x1", d => xScale(d.x1))
        .attr("y1", d => d.y1)
        .attr("x2", d => xScale(d.x2))
        .attr("y2", d => d.y2)
        .attr("stroke", d => d.color)
        .attr("stroke-width", 10)
        .attr("fill", "none")
        
        .on("mouseover",showTooltip) // Show tooltip on mouseover
        .on("mousemove", (d) => {
            tooltip
            .style('left', d.pageX-250+'px') // 設定tooltips位置
            .style('top', d.pageY-280+'px')
        })
        .on("mouseout", hideTooltip); // Hide tooltip on mouseout

        //add scale axis (不同svg width 記得改range)
        var scale = d3.scaleLinear()
                        .domain([0,maxX2])
                        .range([10,1250]);
        const xAxis = d3.axisBottom(scale);

        // Append a group element to the SVG to hold the axis
        svg.append("g")
        .attr("class", "x-axis") // You can add a class for styling
        .attr("transform", `translate(0, ${120})`) // Adjust the y position as needed
        .call(xAxis);
        
        // Style the axis ticks and text
        svg.selectAll(".x-axis text")
        .style("text-anchor", "middle") // Adjust text alignment as needed
        .attr("dy", "1em"); // Adjust the vertical position of the text

//for spliced d3 line & tooltips (clash)  記得改css

        const svg_c = d3.select("#clash_d3");
        const tooltip_c = d3.select(".tooltip_c");
        //to match the line with the svg width
        const svgWidth_c = +svg_c.attr("width");
        //const maxX2 = d3.max(search_d3_line, d => d.x2);

        // Create an xScale based on the maximum x2 value
        const xScale_c = d3.scaleLinear()
            .domain([0, maxX2])
            .range([0, svgWidth_c]);


        function showTooltip_c(d) {
            tooltip_c.style("opacity", 1) // 顯示tooltips
            tooltip_c.html(`<table role="grid" aria-describedby="originalResult-myTable_info" style="width: 1300px; border: 5px solid white; border-collapse: collapse;">
                          <tr>
                              <th>regulator</th>
                              <th>read count</th>
                              <th>mutation</th>
                              <th>identified region</th>
                          </tr>
                          <tr>
                          <td>${d.target.__data__.targetrnaname}</td>
                          <td>${d.target.__data__.readcount}</td>
                          <td>-</td>
                          <td>${d.target.__data__.targetrnaregionfoundinclashread}</td>
                          </tr>
                          <tr>
                              <th>Predicted binding site from miRanda</th>
                              <th>miRanda energy</th>
                              <th>miRanda pairing</th>
                          </tr>
                          <tr>
                              <td>${d.target.__data__.mirandabindingsite}</td>
                              <td>${d.target.__data__.mirandaenergy}</td>
                              <td ${d.target.__data__.miRanda_pairing}</td>
                          </tr>
                          <tr>
                              <th>Predicted binding site from RNAup</th>
                              <th>RNAup energy</th>
                              <th>RNAup pairing</th>
                          </tr>
                          <tr>
                          <td>${d.target.__data__.rnaupbindingsite}</td>
                          <td>${d.target.__data__.rnaupscore}</td>
                          <td ${d.target.__data__.rnaup_pairing}</td>
                          </tr>
                        </table>`); //呈現文字在html 用 target.__data__ 找
            }
            
        function hideTooltip_c() { tooltip_c.style("opacity", 0); }
        svg_c.selectAll("line")
        .data(clash_d3_line)
        .enter().append("line")
        .attr("x1", d => xScale_c(d.x1))
        .attr("y1", d => d.y1)
        .attr("x2", d => xScale_c(d.x2))
        .attr("y2", d => d.y2)
        .attr("stroke", d => d.color)
        .attr("stroke-width", 10)
        .attr("fill", "none")

        .on("mouseover",showTooltip_c) // Show tooltip on mouseover
        .on("mousemove", (d) => {
            tooltip_c
            .style('left', d.pageX-1300+'px') // 設定tooltips位置
            .style('top', d.pageY-450+'px')
        })
        .on("mouseout", hideTooltip_c); // Hide tooltip on mouseout

     



            $('#table1').DataTable({
                searching: true, 
                paging: true, 
                info: true,
                //滑動功能
                scrollCollapse: true, 
                scrollX: "1000px",
                scrollY: "1000px", 
                data: response.table_list,
                columns: [
                    { data: 'smallrnaname', title: "miRNA" },
                    { data: 'targetrnaname', title: "mRNA" },
                    { data: 'readcount', title: "read count" },                    
                    { data: 'targetrnaregionfoundinclashread', title:"CLASH identified region"},
                    { data: 'mirandabindingsite', title: "miranda binding site" },
                    { data: 'mirandaenergy', title: "Miranda energy" },
                    { data: 'miRanda_pairing', title: "miRanda pairing(top:Transcript, Bottom:Regulator)" },
                    { data: 'rnaupbindingsite', title: "RNAup binding site" },
                    { data: 'rnaupscore', title: "RNAup score " },
                    { data: 'rnaup_pairing', title: "RNAup pairing (top:Transcript, Bottom:Regulator)" },
                ],
                /*auto refrash*/
                destroy:true,})



            $('#submit').click(function(event){
                event.preventDefault();

            document.getElementById('tag1').innerHTML = tag;
                
                const check_list = [];
                let anyChecked = false;
                for (let i = 0; i < select_list.length; i++) {
                    
                    const selectElement = $('#' + select_list[i] + '_selection');
                    if (selectElement.length > 0) {
                        if (selectElement.is(':checked')) {
                            check_list.push(select_list[i]);
                            console.log(select_list[i] + ' is checked.');
                            anyChecked = true;                 
                        } else {
                            console.log(select_list[i] + ' is not checked.');
                        }
                    }
                }
                
                if (!anyChecked) {
                    check_list.push('all'); // If no checkboxes were checked, add 'all' to the list
                }
                console.log(check_list);
                $.ajax({
                    headers: { 'X-CSRFToken': csrf_token },
                    type: 'POST',
                    url: '/web_tool/search_data2/', 
                    data: {'transcript_id':transcript,'check_list': check_list.join(',')},
                        success: function(response){
                        search_d3_line=response.search_d3_line
                        clash_d3_line=response.clash_d3_line

                    //for spliced d3 line & tooltips (spliced)
                    const svg = d3.select("#search_d3");
                    const tooltip = d3.select(".tooltip");
                    //to match the line with the svg width
                    const svgWidth = +svg.attr("width");
                    const maxX2 = d3.max(search_d3_line, d => d.x2);
        
                    // Create an xScale based on the maximum x2 value
                    const xScale = d3.scaleLinear()
                        .domain([0, maxX2])
                        .range([0, svgWidth]);
        
        
                    function showTooltip(d) {
                        tooltip.style("opacity", 1) // 顯示tooltips
                        tooltip.html(`Type:${d.target.__data__.Type}<br>Start:${d.target.__data__.start}<br>End:${d.target.__data__.end}`); //呈現文字在html 用 target.__data__ 找
                        }
                        
                    function hideTooltip() { tooltip.style("opacity", 0); }
                    svg.selectAll("line")
                    .data(search_d3_line)
                    .enter().append("line")
                    .attr("x1", d => xScale(d.x1))
                    .attr("y1", d => d.y1)
                    .attr("x2", d => xScale(d.x2))
                    .attr("y2", d => d.y2)
                    .attr("stroke", d => d.color)
                    .attr("stroke-width", 10)
                    .attr("fill", "none")
                    
                    .on("mouseover",showTooltip) // Show tooltip on mouseover
                    .on("mousemove", (d) => {
                        tooltip
                        .style('left', d.pageX-250+'px') // 設定tooltips位置
                        .style('top', d.pageY-280+'px')
                    })
                    .on("mouseout", hideTooltip); // Hide tooltip on mouseout
        
                    //add scale axis (不同svg width 記得改range)
                    var scale = d3.scaleLinear()
                                    .domain([0,maxX2])
                                    .range([10,1250]);
                    const xAxis = d3.axisBottom(scale);
        
                    // Append a group element to the SVG to hold the axis
                    svg.append("g")
                    .attr("class", "x-axis") // You can add a class for styling
                    .attr("transform", `translate(0, ${120})`) // Adjust the y position as needed
                    .call(xAxis);
                    
                    // Style the axis ticks and text
                    svg.selectAll(".x-axis text")
                    .style("text-anchor", "middle") // Adjust text alignment as needed
                    .attr("dy", "1em"); // Adjust the vertical position of the text
 
    //for spliced d3 line & tooltips (clash)
            const svg_c = d3.select("#clash_d3");
            const tooltip_c = d3.select(".tooltip_c");
            //to match the line with the svg width
            const svgWidth_c = +svg_c.attr("width");
            //const maxX2 = d3.max(search_d3_line, d => d.x2);
    
            // Create an xScale based on the maximum x2 value
            const xScale_c = d3.scaleLinear()
                .domain([0, maxX2])
                .range([0, svgWidth_c]);
    
    
            function showTooltip_c(d) {
                tooltip_c.style("opacity", 1) // 顯示tooltips
                tooltip_c.html(`<table role="grid" aria-describedby="originalResult-myTable_info" style="width: 1300px; border: 5px solid white; border-collapse: collapse;">
                              <tr>
                                  <th>regulator</th>
                                  <th>read count</th>
                                  <th>mutation</th>
                                  <th>identified region</th>
                              </tr>
                              <tr>
                              <td>${d.target.__data__.targetrnaname}</td>
                              <td>${d.target.__data__.readcount}</td>
                              <td>-</td>
                              <td>${d.target.__data__.targetrnaregionfoundinclashread}</td>
                              </tr>
                              <tr>
                                  <th>Predicted binding site from miRanda</th>
                                  <th>miRanda energy</th>
                                  <th>miRanda pairing</th>
                              </tr>
                              <tr>
                                  <td>${d.target.__data__.mirandabindingsite}</td>
                                  <td>${d.target.__data__.mirandaenergy}</td>
                                  <td ${d.target.__data__.miRanda_pairing}</td>
                              </tr>
                              <tr>
                                  <th>Predicted binding site from RNAup</th>
                                  <th>RNAup energy</th>
                                  <th>RNAup pairing</th>
                              </tr>
                              <tr>
                              <td>${d.target.__data__.rnaupbindingsite}</td>
                              <td>${d.target.__data__.rnaupscore}</td>
                              <td ${d.target.__data__.rnaup_pairing}</td>
                              </tr>
                            </table>`); //呈現文字在html 用 target.__data__ 找
                }
                
            function hideTooltip_c() { tooltip_c.style("opacity", 0); }
            svg_c.selectAll("line")
            .data(clash_d3_line)
            .enter().append("line")
            .attr("x1", d => xScale_c(d.x1))
            .attr("y1", d => d.y1)
            .attr("x2", d => xScale_c(d.x2))
            .attr("y2", d => d.y2)
            .attr("stroke", d => d.color)
            .attr("stroke-width", 10)
            .attr("fill", "none")
    
            .on("mouseover",showTooltip_c) // Show tooltip on mouseover
            .on("mousemove", (d) => {
                tooltip_c
                .style('left', d.pageX-1300+'px') // 設定tooltips位置
                .style('top', d.pageY-450+'px')
            })
            .on("mouseout", hideTooltip_c); // Hide tooltip on mouseout
                         

            $('#table1').DataTable({
                searching: true, 
                paging: true, 
                info: true,
                //滑動功能
                scrollCollapse: true, 
                scrollX: "1000px",
                scrollY: "1000px", 
                data: response.table_list,
                columns: [
                    { data: 'smallrnaname', title: "miRNA" },
                    { data: 'targetrnaname', title: "mRNA" },
                    { data: 'readcount', title: "read count" },                    
                    { data: 'targetrnaregionfoundinclashread', title:"CLASH identified region"},
                    { data: 'mirandabindingsite', title: "miranda binding site" },
                    { data: 'mirandaenergy', title: "Miranda energy" },
                    { data: 'miRanda_pairing', title: "miRanda pairing(top:Transcript, Bottom:Regulator)" },
                    { data: 'rnaupbindingsite', title: "RNAup binding site" },
                    { data: 'rnaupscore', title: "RNAup score " },
                    { data: 'rnaup_pairing', title: "RNAup pairing (top:Transcript, Bottom:Regulator)" },
                ],
                /*auto refrash*/
                destroy:true,})

                    },
                    error: function(){
                        alert('Something error');
                    }
                });
            });
        
        },
        error: function(){
            alert('Something error');
        }  
    })
    
});
