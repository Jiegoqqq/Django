$(document).ready(function(){
    $('#myDataTable').DataTable(
        {    
            "processing": true,
            "serverSide": true,
            "scrollCollapse": true,
            "scrollX": "1000px",
            "scrollY": "1000px", 
            "ajax": {
                "url": "/update_GeneAnnotation/",
                "type": "GET"
            },
             "columns": [
                {data:'Library Name', title: 'Library Name'},
                {data: 'Gene ID', title: 'Gene ID '},
                {data: 'Gene location', title: 'Gene location'},
                {data: 'Gene expression', title: 'Gene expression'},
                {data: 'Accession number (Best hits in the GenBank)', title: 'Accession number (Best hits in the GenBank)'},
                {data: 'Annotation', title: 'Annotation'},
                {data: 'Species', title: 'Species'},
                {data: 'Blast Score', title: 'Blast Score'},
                {data: 'Expect value', title: 'Expect value'},
                {data: 'Identities', title: 'Identities'},
                {data: 'Frame', title: 'Frame'},
                {data: 'KEGG pathway', title: 'KEGG pathway'},
                {data: 'GO Term', title: 'GO Term'},
                {data: 'Interpro', title: 'Interpro'},
                {data: 'Pfam', title: 'Pfam'},
                {data: 'Swissprot', title: 'Swissprot'},
                {data: 'TrEMBL', title: 'TrEMBL'},
                {data: 'TF_ath', title: 'TF_ath'},
                {data: 'TF_osa', title: 'TF_osa'},
            ]
        })
})