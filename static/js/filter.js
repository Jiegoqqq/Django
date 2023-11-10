$(document).ready(function(){

    $('#submit').click(function(){
    //gene
    var gene = document.getElementById('genelistInput')
    var gene_Value = gene.value;        
    //miRNA
    var miRNA = document.getElementById('miRNAlistInput')
    var miRNA_Value = miRNA.value;        
    //Read count 
    var readcount_mode = document.getElementById('readcount_mode')
    var readcount_mode_Value = readcount_mode.value;
    var readcount = document.getElementById('readcount')
    var readcount_Value = readcount.value; 
    //RNAup score
    var RNAup_score_mode = document.getElementById('RNAup_score_mode')
    var RNAup_score_mode_Value = RNAup_score_mode.value; 
    var RNAup_score = document.getElementById('RNAup_score')
    var RNAup_score_Value = RNAup_score.value; 
    //miRanda energy
    var miranda_energy_mode = document.getElementById('miRanda_energy_mode')
    var miranda_energy_mode_Value = miranda_energy_mode.value; 
    var miranda_energy = document.getElementById('miRanda_energy')
    var miranda_energy_Value = miranda_energy.value; 
    //RNAup max score
    var RNAup_max_score_mode = document.getElementById('RNAup_max_score_mode')
    var RNAup_max_score_mode_Value = RNAup_max_score_mode.value; 
    var RNAup_max_score = document.getElementById('RNAup_max_score')
    var RNAup_max_score_Value = RNAup_max_score.value; 
    //miRanda max energy
    var miranda_max_energy_mode = document.getElementById('miranda_max_energy_mode')
    var miranda_max_energy_mode_Value = miranda_max_energy_mode.value; 
    var miranda_max_energy = document.getElementById('miranda_max_energy')
    var miranda_max_energy_Value = miranda_max_energy.value; 

        
    // use to print value on html console
    console.log('readcount_mode:', readcount_mode_Value);
    console.log('readcount:', readcount_Value);
    console.log('gene_Value:', gene_Value);
    console.log('miRNA_Value:', miRNA_Value);
    console.log('miranda_energy_mode:', miranda_energy_mode_Value);
    console.log('miranda_energy:', miranda_energy_Value);
    


    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: 'POST',
        url: '/web_tool/filter_data/', 
        data: { 'gene':gene_Value,'miRNA':miRNA_Value,
                'readcount_mode':readcount_mode_Value,'readcount':readcount_Value,
                'RNAup_score_mode':RNAup_score_mode_Value,'RNAup_score':RNAup_score_Value,
                'miranda_energy_mode':miranda_energy_mode_Value,'miranda_energy':miranda_energy_Value,
                'RNAup_max_score_mode':RNAup_max_score_mode_Value,'RNAup_max_score':RNAup_max_score_Value,
                'miranda_max_energy_mode':miranda_max_energy_mode_Value,'miranda_max_energy':miranda_max_energy_Value,}
                ,
 
        success: function(response){

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
                    { data: 'id', title: "Gene ID" },
                    { data: 'readcount', title: "read count" },                    
                    { data: 'targetrnaregionfoundinclashread', title:"CLASH identified region"},
                    { data: 'mirandabindingsite', title: "miranda binding site (minimum)" },
                    { data: 'mirandaenergy', title: "Miranda energy (minimum)" },
                    { data: 'miRanda_minpairing', title: "miRanda pairing (minimum) (top:Transcript, Bottom:Regulator)" },
                    { data: 'rnaupbindingsite', title: "RNAup binding site (minimum)" },
                    { data: 'rnaupscore', title: "RNAup score (minimum)" },
                    { data: 'rnaup_minpairing', title: "RNAup pairing (minimum) (top:Transcript, Bottom:Regulator)" },
                    { data: 'mirandamaxbindingsite', title: "Miranda binding site (maximum)" },        
                    { data: 'mirandamaxenergy', title: "Miranda energy (maximum)" },
                    { data: 'miRanda_maxpairing',title:"miRanda pairing (maximum) (top:Transcript, Bottom:Regulator)"},
                    { data: 'rnaupmaxbindingsite', title: "RNAup Max binding site" },
                    { data: 'rnaupmaxscore', title: "RNAup score (maximum)" },
                    { data: 'rnaup_maxpairing', title: "RNAup pairing (maximum) (top:Transcript, Bottom:Regulator)" },

                    // { data: 'smallrnaregionfoundinclashread', title: "Small RNA Region Found in CLASH Read" },
                    // { data: 'regiononclashreadidentifiedastargetrna', title: "Region on CLASH Read identified as Target RNA" },
                    // { data: 'mirandascore',title:"Miranda score"},
                    // { data: 'start',title:"start"},
                    // { data: 'end',title:"end"},
                ],
                /*auto refrash*/
                destroy:true,})


        },
        error: function(){
            alert('Something error');
            },
        });
    });
    
});