document.addEventListener('DOMContentLoaded', function() {
    //計時器的部份
    const spinnerContainer = document.getElementById('spinner-container');//
    const timerElement = document.getElementById('timer');//
    var timerValue = 0;//
    let timerInterval;//
  
    function updateTimerAndSpinner() {//
      timerElement.textContent = timerValue;
      timerValue++;
    }
    //把計時器變成可視
    spinnerContainer.style.display = 'flex';//
    // 启动计时器（每秒更新一次）
    timerInterval = setInterval(updateTimerAndSpinner, 1000);//
    // var globalCancerKind;
    // $("#container").hide();
    // $("#image1").hide();
    // $("#download_button").hide();
    //初始先用ajax傳輸gene name的autocomplete資料



    // $.ajax({
    //     url: '/web_tool/gene_name_data/',  // 
    //     type: 'POST',
    //     // dataType: 'json',
    //     success: function(data) {
    //         var Gene_name = data.gene_names;
    //         $(function() {
    //             $("#input").autocomplete({
    //                 source: Gene_name, // Provide the source data
    //                 minLength: 1, 
    //             });
    //         });
    //     },
    //     error: function(error) {
    //         console.log('Error:', error);
    //     }
    // });



    // $('#submit').click(function(){
        // $("#message").html('<div class="alert alert-warning">' + 'analysis running !' + '</div>');
        // var gene_name = $("#input").val();

        var URL = document.URL; //用這個可以得到現在的URL網址
        react = URL.replace('http://127.0.0.1:8000/web_tool/cancer_web/',''); //得到transcript id
        react_list = react.split("/");
        gene_name = react_list[0];
        survival_input_high = react_list[1];
        survival_input_low = react_list[2];
        survival_input_days = react_list[3];
        stage = react_list[4];

        $.ajax({
            type: 'POST',
            url: '/web_tool/cancer_data/', 
            data: {'gene_name':gene_name,'survival_input_high':survival_input_high,'survival_input_low':survival_input_low,'survival_input_days':survival_input_days,'stage':stage },
            success: function(response){ 
                $("#message").html('<div class="alert alert-warning">' + 'complete !' + '</div>');
                // 清除计时器
                clearInterval(timerInterval);//

                // 隐藏 Spinner
                spinnerContainer.style.display = 'none';//

                let image1 = `
                <!-- png圖片 -->
                <img src = "data:image/png;base64,` + response.image_data +`"; alt="Embedded Image">
                <br>
                <div class="center-container">
                <button id="downloadButton">Download CSV</button>
                </div>`;
                document.getElementById('button1').innerHTML = image1;
                // $("#container").toggle();
                // $("#image1").toggle();
                // $("#download_button").toggle();
                //給下載按鈕功能的
                var csvData = response.csv_data;
                // 當按鈕被點擊時執行下載邏輯
                document.getElementById('downloadButton').addEventListener('click', function() {
                // 將CSV字串轉換成Blob物件
                    var blob = new Blob([csvData], { type: 'text/csv' });
                    // 產生一個下載連結
                    var downloadLink = document.createElement('a');
                    downloadLink.href = window.URL.createObjectURL(blob);
                    downloadLink.download = 'data.csv';
                    downloadLink.textContent = 'Download CSV';
                    // 模擬點擊連結以啟動下載
                    downloadLink.click();
                    // 移除創建的連結
                    document.body.removeChild(downloadLink);
                });
            },
            error: function(){
                $("#message").html('<div class="alert alert-warning">' + 'check again !' + '</div>');
                /*alert('Something error');*/
                
            },
        });
        $('#plot_submit').click(function(){
            var survival_input_low = $("#survival_input_low").val();
            var survival_input_high = $("#survival_input_high").val();
            var survival_input_days = $("#survival_input_days").val();
            var stage = $("#survival_select").val();
            clearInterval(timerInterval);//
            spinnerContainer.style.display = 'flex';//
            // 启动计时器（每秒更新一次）
            timerInterval = setInterval(updateTimerAndSpinner, 1000);//
        $.ajax({
            type: 'POST',
            url: '/web_tool/cancer_plot_data/', 
            data: {'gene_name':gene_name,'survival_input_low':survival_input_low, 'survival_input_high':survival_input_high, 'survival_input_days':survival_input_days,'stage':stage},
            success: function(response){
                // 清除计时器
                clearInterval(timerInterval);//
        
                // 隐藏 Spinner
                spinnerContainer.style.display = 'none';//

                let image2 = `
                <!-- png圖片 -->
                <img src = "data:image/png;base64,` + response.image_data +`"; alt="Embedded Image">
                <br>
                <div class="center-container">
                <button id="downloadButton">Download CSV</button>
                </div>`;
                document.getElementById('button1').innerHTML = image2;

                //給下載按鈕功能的
                var csvData = response.csv_data;
                // 當按鈕被點擊時執行下載邏輯
                document.getElementById('downloadButton').addEventListener('click', function() {
                // 將CSV字串轉換成Blob物件
                    var blob = new Blob([csvData], { type: 'text/csv' });
                    // 產生一個下載連結
                    var downloadLink = document.createElement('a');
                    downloadLink.href = window.URL.createObjectURL(blob);
                    downloadLink.download = 'data.csv';
                    downloadLink.textContent = 'Download CSV';
                    // 模擬點擊連結以啟動下載
                    downloadLink.click();
                    // 移除創建的連結
                    document.body.removeChild(downloadLink);
                });
            },
            error: function(){

            }
        })
        });


        
    });
