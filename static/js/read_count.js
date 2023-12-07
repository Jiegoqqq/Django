$(document).ready(function(){
    var URL = document.URL; //用這個可以得到現在的URL網址
    transcript = URL.replace('http://127.0.0.1:8000/web_tool/read_count/',''); //得到transcript id
    let tag =`        <h2 class="card-title text-center mt-2" style="font-size: 2em;">CLASH identified piRNA target sites (Table View)</h2>    
    <div id="match_hint" class="col" style="text-align: right;">
        <div id="non-GU" style="display:inline-block;border:1px solid black;background-color:#fffb13;">
            &nbsp;&nbsp;&nbsp;&nbsp;
        </div>&nbsp;<span><b>&nbsp;non-GU mismatch&nbsp;</b></span>
        <div id="GU" style="display:inline-block;border:1px solid black;background-color:#a1c2e4;">
            &nbsp;&nbsp;&nbsp;&nbsp;
        </div>&nbsp;<span><b>&nbsp;GU mismatch&nbsp;</b></span>
        <div id="first_pos" style="display:inline-block;border:1px solid black;background-color:#b3d186;">
            &nbsp;&nbsp;&nbsp;&nbsp;
        </div>&nbsp;<span><b>&nbsp;mismatch at the 1st position of piRNA&nbsp;</b></span>
        <div id="bulge_hint" style="display:inline-block;border:1px solid black;background-color:#13ffe0;">
            &nbsp;&nbsp;&nbsp;&nbsp;
        </div>&nbsp;<span><b>&nbsp;bulge&nbsp;</b></span>
        <div id="mutation_hint" style="display:inline-block;">
            <font color="red">&nbsp;M&nbsp;</font>
        </div>&nbsp;<span><b>&nbsp;Mutation&nbsp;</b></span>
        <div class="text-danger" style="display:inline-block;">|&nbsp;&nbsp;|</div>&nbsp;<span><b>&nbsp;seed region&nbsp;</b></span>
    </div>
    
    <table class="table table-bordered" id="table1" ></table><br> 
    <div id ='piRTarBase_list'></div>  
    <div class="tooltip" style="opacity: 0;"></div>
    <svg width="1250" height="150" id="search_d3"></svg>
    <div id ='A22G'></div>  
    `;
    document.getElementById('tag1').innerHTML = tag;
    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        url: '/web_tool/read_count_data/', 
        data: {'transcript_id':transcript,},
 
         success: function(response){
            check_box=response.check_box



            $('#target_table').DataTable({
                "data": check_box,
                "columns": [
                    {
                        "data": null,
                        "defaultContent": '<input type="checkbox" class="pirtarbase_checkbox" >'
                        
                    },

                    { "data": "RNANAME" }
                ],
                "columnDefs": [
                    {
                        "targets": 0,
                        "orderable": false,
                        "className": 'select-checkbox',
                        "data": null,
                        "defaultContent": ""
                    }
                ],

                "select": {
                    "style": "multi",
                    "selector": 'td:first-child'
                },
            // 在每行创建时为复选框设置不同的ID
                "createdRow": function (row, data, dataIndex) {
                    $('td:eq(0)', row).find('.pirtarbase_checkbox').attr('id', data.RNANAME);
                }
            });

            // Handle "Select All" checkbox
        // function toggleAll(source) {
        //     var checkboxes = table.column(0).nodes().to$().find(':checkbox');
        //     checkboxes.prop('checked', source.checked);
        // }
            
        const firstCheckbox = document.querySelector('.pirtarbase_checkbox');
        firstCheckbox.checked = true;
        
  function generatePopoverContent(data) {
    // Customize this function to generate the popover content based on the data
    return `
    <div class="tippy-content" data-state="visible" style="transition-duration: 300ms;">
        <table class="table" style="color: white; id='table123'">
            <thead>
                <tr>
                    <th>CLASH read ID</th>
                    <th>CLASH read sequence</th>
                    <th>Region identified by piRNA</th>
                    <th>Region identified by target RNA</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${data['CLASH read ID']}</td>
                    <td><font color="green">${data['CLASH read sequence']}</font></td>
                    <td>${data['Region identified by piRNA']}</td>
                    <td>${data['Region identified by target RNA']}</td>
                </tr>
            </tbody>
        </table>
    </div>`;
}
        
        $('#table1').DataTable({
            searching: true, 
            paging: true, 
            info: true,
            //滑動功能
            scrollCollapse: true, 
            scrollX: "1500px",
            scrollY: "1500px", 
            data: response.table_list,
            columns: [
                {
                    data: 'CLASH read ID',
                    title: 'CLASH read ID',
                    render: function (data, type, full, meta) {
                        if (type === 'display') {
                            const buttonHtml = `
                                <div class="button-container" style="position: relative;">
                                    <div class="tippy-box" data-state="visible" tabindex="-1" data-animation="fade" role="tooltip" data-placement="bottom" style="max-width: 2500px; transition-duration: 300ms;">
                                        <div class="custom-tooltip-content" data-state="visible" style="transition-duration: 300ms; display: none;">
                                            ${generatePopoverContent(full)}
                                        </div>
                                    </div>
                                    <div class="tippy-arrow" style="position: absolute; left: 50%; transform: translateX(-50%);"></div>
                                    <button type="button" class="btn btn-outline-secondary clash-info" 
                                        data-tippy-allowhtml="true" 
                                        data-tippy-maxwidth="1500" 
                                        data-tippy-trigger="click" 
                                        data-tippy-interactive="true" 
                                        data-tippy-placement="top" 
                                        aria-expanded="false">
                                        ${data}
                                    </button>
                                </div>`;
                            return buttonHtml;
                        }
                        return data;
                    }
                },
                { data: 'hybrid Count', title: "hybrid Count" },
                { data: 'Clash identified region', title: "Clash identified region" },                    
                { data: 'predicted binding site from pirScan', title:"predicted binding site from pirScan"},
                { data: 'pirScan targeting score', title: "pirScan targeting score" },
                { data: 'WT_WAGO122G(pirScan)', title: "WT_WAGO122G(pirScan)" },
                { data: 'prg-1 mutant WAGO122G(pirScan)', title: "prg-1 mutant WAGO122G(pirScan)" },
                { data: '22G-RNA fold change(pirScan)', title: "22G-RNA fold change(pirScan)" },
                { data: 'pirScan_pairing', title: "pirScan_min_ex_target_rna_sequence" },
                { data: 'predicted binding site from RNAup', title: "predicted binding site from RNAup" },
                { data: 'RNAup binding energy', title: "RNAup binding energy" },
                { data: 'WT_WAGO122G(RNAup)', title: "WT_WAGO122G(RNAup)" },
                { data: 'prg-1 mutant WAGO122G(RNAup)', title: "prg-1 mutant WAGO122G(RNAup)" },
                { data: '22G-RNA fold change(RNAup)', title: "22G-RNA fold change(RNAup)" },
                { data: 'rnaup_pairing', title: "rnaup_max_ex_target_rna_sequence" },
            ],
            columnDefs: [
                {
                    targets: 5, // 0-based index for the column
                    createdCell: function (td, cellData, rowData, row, col) {
                        // Check if the cell data can be converted to an integer
                        const wtWagoValue = parseInt(cellData);
                        if (!isNaN(wtWagoValue)) {
                            // Change the cell's text color to red
                            $(td).css('color', 'red');
                            // Set the cell's text to the integer value
                            $(td).text(wtWagoValue);
                        }
                    },
                },
                {
                    targets: 11, // 0-based index for the column
                    createdCell: function (td, cellData, rowData, row, col) {
                        // Check if the cell data can be converted to an integer
                        const wtWagoValue = parseInt(cellData);
                        if (!isNaN(wtWagoValue)) {
                            // Change the cell's text color to red
                            $(td).css('color', 'red');
                            // Set the cell's text to the integer value
                            $(td).text(wtWagoValue);
                        }
                    },
                },
            ],

            /*auto refrash*/
            destroy:true,});
            // 更改 aria-expanded 的狀態
            tippy('.clash-info', {
                onShow(instance) {
                    const button = instance.reference;
                    // Set aria-expanded attribute to 'true'
                    button.setAttribute('aria-expanded', 'true');
                },
                onHide(instance) {
                    const button = instance.reference;
                    // Set aria-expanded attribute to 'false' when hiding the tooltip
                    button.setAttribute('aria-expanded', 'false');
                }
            });
//for d3
        search_d3_line=response.search_d3_line
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
                .attr("stroke-width", 20)
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
                .attr("transform", `translate(0, ${100})`) // Adjust the y position as needed
                .call(xAxis);
                
                // Style the axis ticks and text
                svg.selectAll(".x-axis text")
                .style("text-anchor", "middle") // Adjust text alignment as needed
                .attr("dy", "1em"); // Adjust the vertical position of the text


//for piRTarBase_list
                piRTarBase_list = response.piRTarBase_list
                // Create a tooltip_c div element
                const tooltip_c = d3.select("#piRTarBase_list")
                .append("div")
                .attr("class", "tooltip_c")
                .style("opacity", 0);

                // Create an SVG element and set its width and height
                const maxY = d3.max(piRTarBase_list, d => d.y);
                const svg_c = d3.select("#piRTarBase_list")
                .append("svg")
                .attr("width", 1250) // Set the desired width
                .attr("height", maxY) // Set the desired height
                .attr("id", "piRTarBase");

                // Continue using your code
                const svgWidth_c = +svg_c.attr("width");

                // Create an xScale based on the maximum x2 value
                const xScale_c = d3.scaleLinear()
                    .domain([0, maxX2])
                    .range([0, svgWidth_c]);


                function showTooltip_c(d) {
                    tooltip_c.style("opacity", 1) // 顯示tooltips
                    tooltip_c.html(`<table role="grid" aria-describedby="originalResult-myTable_info" style="width: 1300px; border: 5px solid white; border-collapse: collapse;">
                    <tr>
                        <th style="border: 1px solid white; text-align: center;">CLASH_Read_ID</th>
                        <th style="border: 1px solid white; text-align: center;">hybrid_count</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.CLASH_read_ID}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.hybrid_Count}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid white; text-align: center;">predicted_binding_site_from_pirScan</th>
                        <th style="border: 1px solid white; text-align: center;">pirScan_targeting_score</th>
                        <th style="border: 1px solid white; text-align: center;">WT_WAGO122G_pirScan</th>
                        <th style="border: 1px solid white; text-align: center;">prg_1_mutant_WAGO122G_pirScan</th>
                        <th style="border: 1px solid white; text-align: center;">A22G_RNA_fold_change_pirScan</th>
                        <th style="border: 1px solid white; text-align: center;">pirScan_pairing</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.predicted_binding_site_from_pirScan}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.pirScan_targeting_score}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.WT_WAGO122G_pirScan}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.prg_1_mutant_WAGO122G_pirScan}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.A22G_RNA_fold_change_pirScan}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.pirScan_pairing}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid white; text-align: center;">predicted_binding_site_from_RNAup</th>
                        <th style="border: 1px solid white; text-align: center;">RNAup_binding_energy</th>
                        <th style="border: 1px solid white; text-align: center;">WT_WAGO122G_RNAup</th>
                        <th style="border: 1px solid white; text-align: center;">prg_1_mutant_WAGO122G_RNAup</th>
                        <th style="border: 1px solid white; text-align: center;">A22G_RNA_fold_change_RNAup</th>
                        <th style="border: 1px solid white; text-align: center;">rnaup_pairing</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.predicted_binding_site_from_RNAup}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.RNAup_binding_energy}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.WT_WAGO122G_RNAup}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.prg_1_mutant_WAGO122G_RNAup}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.A22G_RNA_fold_change_RNAup}</td>
                        <td style="border: 1px solid white; text-align: center;">${d.target.__data__.rnaup_pairing}</td>
                    </tr>
                </table>
                `); //呈現文字在html 用 target.__data__ 找
                    }
                    
                function hideTooltip_c() { tooltip_c.style("opacity", 0); }
                svg_c.selectAll("line")
                .data(piRTarBase_list)
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
                    .style('left', d.pageX-600+'px') // 設定tooltips位置
                    .style('top', d.pageY-500+'px')
                })
                .on("mouseout", hideTooltip_c); // Hide tooltip on mouseout

//for 22G
                A22_list  = response.A22_list
                // Create a tooltip_c div element
                const tooltip_g = d3.select("#A22G")
                .append("div")
                .attr("class", "tooltip_g")
                .style("opacity", 0);

                // Create an SVG element and set its width and height
                const maxYg = d3.max(A22_list, d => d.A22_value);
                const svgHeight = d3.max(A22_list, d => parseFloat(d.A22_value)); // 取得A22_value的最大值
                const svg_g = d3.select("#A22G")
                .append("svg")
                .attr("width", 1250) // Set the desired width
                .attr("height", svgHeight/20) // Set the desired height
                .attr("id", "A22G");

                // Continue using your code
                const svgWidth_g = +svg_g.attr("width");
                // Create an xScale based on the maximum x2 value
                const xScale_g = d3.scaleLinear()
                    .domain([0, maxX2])
                    .range([0, svgWidth_g]);

                yScale = d3.scaleLinear()
                .domain([0, svgHeight])
                .range([svgHeight, 0]);

                function showTooltip_g(d) {
                    tooltip_g.style("opacity", 1)
                    tooltip_g.html(`${d.target.__data__.A22_value}`); }

                function hideTooltip_g() { tooltip_g.style("opacity", 0); }

                svg_g.selectAll("rect")
                .data(A22_list)
                .enter().append("rect")
                .attr("x", d => xScale_g(parseFloat(d.A22_start)))
                .attr("y", 0)
                .attr("width", d => xScale_g(parseFloat(d.A22_end)) - xScale_g(parseFloat(d.A22_start)))
                .attr("height", d => (svgHeight - yScale(parseFloat(d.A22_value)))/20)
                .attr("fill", d => d.color)
                .on("mouseover",showTooltip_g) // Show tooltip on mouseover
                .on("mousemove", (d) => {
                    tooltip_g
                    .style('left', d.pageX-300+'px') // 設定tooltips位置
                    .style('top', d.pageY-250+'px')
                })
                .on("mouseout", hideTooltip_g); // Hide tooltip on mouseout 

// submit send
    $('#submit').click(function(event){
        event.preventDefault();

    document.getElementById('tag1').innerHTML = tag;
        
        const check_list = [];
        let anyChecked = false;
        for (let i = 0; i < check_box.length; i++) {
            
            const selectElement = $('#' + check_box[i]['RNANAME'] );
            if (selectElement.length > 0) {
                if (selectElement.is(':checked')) {
                    check_list.push(check_box[i]['RNANAME']);
                    console.log(check_box[i]['RNANAME'] + ' is checked.');
                    anyChecked = true;  
                }               
            }
        }
        
        if (!anyChecked) {
            check_list.push('all'); // If no checkboxes were checked, add 'all' to the list
        }
        $.ajax({
            headers: { 'X-CSRFToken': csrf_token },
            type: 'POST',
            url: '/web_tool/read_count_data2/', 
            data: {'transcript_id':transcript,'check_list': check_list.join(',')},
                success: function(response){
                    function generatePopoverContent(data) {
                        // Customize this function to generate the popover content based on the data
                        return `
                        <div class="tippy-content" data-state="visible" style="transition-duration: 300ms;">
                            <table class="table" style="color: white;">
                                <thead>
                                    <tr>
                                        <th>CLASH read ID</th>
                                        <th>CLASH read sequence</th>
                                        <th>Region identified by piRNA</th>
                                        <th>Region identified by target RNA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>${data['CLASH read ID']}</td>
                                        <td><font color="green">${data['CLASH read sequence']}</font></td>
                                        <td>${data['Region identified by piRNA']}</td>
                                        <td>${data['Region identified by target RNA']}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>`;
                    }
                            
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
                                    {
                                        data: 'CLASH read ID',
                                        title: 'CLASH read ID',
                                        render: function (data, type, full, meta) {
                                            if (type === 'display') {
                                                const buttonHtml = `
                                                <div class="button-container">
                                                <div class="tippy-box" data-state="visible" tabindex="-1" data-animation="fade" role="tooltip" data-placement="top" style="max-width: 2500px; transition-duration: 300ms;">
                                                    <div class="custom-tooltip-content" data-state="visible" style="transition-duration: 300ms; display: none;">
                                                        ${generatePopoverContent(full)}
                                                    </div>
                                                </div>
                                                <div class="tippy-arrow" style="position: absolute; left: 50%; transform: translateX(-50%);"></div>
                                                <button type="button" class="btn btn-outline-secondary clash-info" 
                                                    data-tippy-allowhtml="true" 
                                                    data-tippy-maxwidth="1500" 
                                                    data-tippy-trigger="click" 
                                                    data-tippy-interactive="true" 
                                                    data-tippy-placement="top" 
                                                    aria-expanded="false">
                                                    ${data}
                                                </button>
                                            </div>
                                            
                                                `;
                                                return buttonHtml;
                                            }
                                            return data;
                                        }
                                    },
                                    
                                    { data: 'hybrid Count', title: "hybrid Count" },
                                    { data: 'Clash identified region', title: "Clash identified region" },                    
                                    { data: 'predicted binding site from pirScan', title:"predicted binding site from pirScan"},
                                    { data: 'pirScan targeting score', title: "pirScan targeting score" },
                                    { data: 'WT_WAGO122G(pirScan)', title: "WT_WAGO122G(pirScan)" },
                                    { data: 'prg-1 mutant WAGO122G(pirScan)', title: "prg-1 mutant WAGO122G(pirScan)" },
                                    { data: '22G-RNA fold change(pirScan)', title: "22G-RNA fold change(pirScan)" },
                                    { data: 'pirScan_pairing', title: "pirScan_min_ex_target_rna_sequence" },
                                    { data: 'predicted binding site from RNAup', title: "predicted binding site from RNAup" },
                                    { data: 'RNAup binding energy', title: "RNAup binding energy" },
                                    { data: 'WT_WAGO122G(RNAup)', title: "WT_WAGO122G(RNAup)" },
                                    { data: 'prg-1 mutant WAGO122G(RNAup)', title: "prg-1 mutant WAGO122G(RNAup)" },
                                    { data: '22G-RNA fold change(RNAup)', title: "22G-RNA fold change(RNAup)" },
                                    { data: 'rnaup_pairing', title: "rnaup_max_ex_target_rna_sequence" },
                                ],
                                columnDefs: [
                                    {
                                        targets: 5, // 0-based index for the column
                                        createdCell: function (td, cellData, rowData, row, col) {
                                            // Check if the cell data can be converted to an integer
                                            const wtWagoValue = parseInt(cellData);
                                            if (!isNaN(wtWagoValue)) {
                                                // Change the cell's text color to red
                                                $(td).css('color', 'red');
                                                // Set the cell's text to the integer value
                                                $(td).text(wtWagoValue);
                                            }
                                        },
                                    },
                                    {
                                        targets: 11, // 0-based index for the column
                                        createdCell: function (td, cellData, rowData, row, col) {
                                            // Check if the cell data can be converted to an integer
                                            const wtWagoValue = parseInt(cellData);
                                            if (!isNaN(wtWagoValue)) {
                                                // Change the cell's text color to red
                                                $(td).css('color', 'red');
                                                // Set the cell's text to the integer value
                                                $(td).text(wtWagoValue);
                                            }
                                        },
                                    },
                                ],
                    
                                /*auto refrash*/
                                destroy:true,});
                                // 更改 aria-expanded 的狀態
                                tippy('.clash-info', {
                                    onShow(instance) {
                                        const button = instance.reference;
                                        // Set aria-expanded attribute to 'true'
                                        button.setAttribute('aria-expanded', 'true');
                                    },
                                    onHide(instance) {
                                        const button = instance.reference;
                                        // Set aria-expanded attribute to 'false' when hiding the tooltip
                                        button.setAttribute('aria-expanded', 'false');
                                    }
                                });
                    //for d3
                            search_d3_line=response.search_d3_line
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
                                    .attr("stroke-width", 20)
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
                                    .attr("transform", `translate(0, ${100})`) // Adjust the y position as needed
                                    .call(xAxis);
                                    
                                    // Style the axis ticks and text
                                    svg.selectAll(".x-axis text")
                                    .style("text-anchor", "middle") // Adjust text alignment as needed
                                    .attr("dy", "1em"); // Adjust the vertical position of the text
                    
                    
                    //for piRTarBase_list
                                    piRTarBase_list = response.piRTarBase_list
                                    // Create a tooltip_c div element
                                    const tooltip_c = d3.select("#piRTarBase_list")
                                    .append("div")
                                    .attr("class", "tooltip_c")
                                    .style("opacity", 0);
                    
                                    // Create an SVG element and set its width and height
                                    const maxY = d3.max(piRTarBase_list, d => d.y);
                                    const svg_c = d3.select("#piRTarBase_list")
                                    .append("svg")
                                    .attr("width", 1250) // Set the desired width
                                    .attr("height", maxY) // Set the desired height
                                    .attr("id", "piRTarBase");
                    
                                    // Continue using your code
                                    const svgWidth_c = +svg_c.attr("width");
                    
                                    // Create an xScale based on the maximum x2 value
                                    const xScale_c = d3.scaleLinear()
                                        .domain([0, maxX2])
                                        .range([0, svgWidth_c]);
                    
                    
                                    function showTooltip_c(d) {
                                        tooltip_c.style("opacity", 1) // 顯示tooltips
                                        tooltip_c.html(`<table role="grid" aria-describedby="originalResult-myTable_info" style="width: 1300px; border: 5px solid white; border-collapse: collapse;">
                                        <tr>
                                            <th style="border: 1px solid white; text-align: center;">CLASH_Read_ID</th>
                                            <th style="border: 1px solid white; text-align: center;">hybrid_count</th>
                                        </tr>
                                        <tr>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.CLASH_read_ID}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.hybrid_Count}</td>
                                        </tr>
                                        <tr>
                                            <th style="border: 1px solid white; text-align: center;">predicted_binding_site_from_pirScan</th>
                                            <th style="border: 1px solid white; text-align: center;">pirScan_targeting_score</th>
                                            <th style="border: 1px solid white; text-align: center;">WT_WAGO122G_pirScan</th>
                                            <th style="border: 1px solid white; text-align: center;">prg_1_mutant_WAGO122G_pirScan</th>
                                            <th style="border: 1px solid white; text-align: center;">A22G_RNA_fold_change_pirScan</th>
                                            <th style="border: 1px solid white; text-align: center;">pirScan_pairing</th>
                                        </tr>
                                        <tr>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.predicted_binding_site_from_pirScan}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.pirScan_targeting_score}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.WT_WAGO122G_pirScan}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.prg_1_mutant_WAGO122G_pirScan}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.A22G_RNA_fold_change_pirScan}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.pirScan_pairing}</td>
                                        </tr>
                                        <tr>
                                            <th style="border: 1px solid white; text-align: center;">predicted_binding_site_from_RNAup</th>
                                            <th style="border: 1px solid white; text-align: center;">RNAup_binding_energy</th>
                                            <th style="border: 1px solid white; text-align: center;">WT_WAGO122G_RNAup</th>
                                            <th style="border: 1px solid white; text-align: center;">prg_1_mutant_WAGO122G_RNAup</th>
                                            <th style="border: 1px solid white; text-align: center;">A22G_RNA_fold_change_RNAup</th>
                                            <th style="border: 1px solid white; text-align: center;">rnaup_pairing</th>
                                        </tr>
                                        <tr>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.predicted_binding_site_from_RNAup}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.RNAup_binding_energy}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.WT_WAGO122G_RNAup}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.prg_1_mutant_WAGO122G_RNAup}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.A22G_RNA_fold_change_RNAup}</td>
                                            <td style="border: 1px solid white; text-align: center;">${d.target.__data__.rnaup_pairing}</td>
                                        </tr>
                                    </table>
                                    `); //呈現文字在html 用 target.__data__ 找
                                        }
                                        
                                    function hideTooltip_c() { tooltip_c.style("opacity", 0); }
                                    svg_c.selectAll("line")
                                    .data(piRTarBase_list)
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
                                        .style('left', d.pageX-600+'px') // 設定tooltips位置
                                        .style('top', d.pageY-500+'px')
                                    })
                                    .on("mouseout", hideTooltip_c); // Hide tooltip on mouseout
                    
                    //for 22G
                                    A22_list  = response.A22_list
                                    // Create a tooltip_c div element
                                    const tooltip_g = d3.select("#A22G")
                                    .append("div")
                                    .attr("class", "tooltip_g")
                                    .style("opacity", 0);
                    
                                    // Create an SVG element and set its width and height
                                    const maxYg = d3.max(A22_list, d => d.A22_value);
                                    const svgHeight = d3.max(A22_list, d => parseFloat(d.A22_value)); // 取得A22_value的最大值
                                    const svg_g = d3.select("#A22G")
                                    .append("svg")
                                    .attr("width", 1250) // Set the desired width
                                    .attr("height", svgHeight/20) // Set the desired height
                                    .attr("id", "A22G");
                    
                                    // Continue using your code
                                    const svgWidth_g = +svg_g.attr("width");
                                    // Create an xScale based on the maximum x2 value
                                    const xScale_g = d3.scaleLinear()
                                        .domain([0, maxX2])
                                        .range([0, svgWidth_g]);
                    
                                    yScale = d3.scaleLinear()
                                    .domain([0, svgHeight])
                                    .range([svgHeight, 0]);
                    
                                    function showTooltip_g(d) {
                                        tooltip_g.style("opacity", 1)
                                        tooltip_g.html(`${d.target.__data__.A22_value}`); }
                    
                                    function hideTooltip_g() { tooltip_g.style("opacity", 0); }
                    
                                    svg_g.selectAll("rect")
                                    .data(A22_list)
                                    .enter().append("rect")
                                    .attr("x", d => xScale_g(parseFloat(d.A22_start)))
                                    .attr("y", 0)
                                    .attr("width", d => xScale_g(parseFloat(d.A22_end)) - xScale_g(parseFloat(d.A22_start)))
                                    .attr("height", d => (svgHeight - yScale(parseFloat(d.A22_value)))/20)
                                    .attr("fill", d => d.color)
                                    .on("mouseover",showTooltip_g) // Show tooltip on mouseover
                                    .on("mousemove", (d) => {
                                        tooltip_g
                                        .style('left', d.pageX-300+'px') // 設定tooltips位置
                                        .style('top', d.pageY-250+'px')
                                    })
                                    .on("mouseout", hideTooltip_g); // Hide tooltip on mouseout 

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

$(document).on('click', '.clash-info', function() {
    const button = $(this);
    const container = button.closest('.button-container');
    const table = container.find('.custom-tooltip-content');
    
    // 检查表格的显示状态
    const isTableVisible = table.is(':visible');
    
    // 切换表格的显示/隐藏状态
    if (isTableVisible) {
        table.hide();
    } else {
        table.show();
    }
});


