document.addEventListener('DOMContentLoaded', function() {
    //計時器的部份
    const spinnerContainer = document.getElementById('spinner-container');//
    const timerElement = document.getElementById('timer');//
    let timerValue = 0;//
    let timerInterval;//
  
    function updateTimerAndSpinner() {//
      timerElement.textContent = timerValue;
      timerValue++;
    }
  
    $('#submit').click(function() {
      // 显示 Spinner
      spinnerContainer.style.display = 'flex';//
      // 启动计时器（每秒更新一次）
      timerInterval = setInterval(updateTimerAndSpinner, 1000);//
  
      // 获取输入值
      var select_cancer = document.getElementById('select_cancer');
      var select_cancer_Value = select_cancer.value;
      var select_stage = document.getElementById('select_stage');
      var select_stage_Value = select_stage.value;
      var High_Percentile_input = $("#High_Percentile_input").val();
      var Low_Percentile_input = $("#Low_Percentile_input").val();
      var Pvalue_input = $("#Pvalue_input").val();
  
        let result_table = `<div class="card "> 
        <div class="card-header">
        <h4 style="text-align:left"><b><i class="fas fa-user-cog"></i>  </b></h4> 
        </div>  
        <div class="card-body">
            <div class="centered">
                <p style="font-weight: bold; font-size: 20px;"> Result </p>
            </div>
            <div class="checkbox-container">
                <p style="font-weight: bold;">Search Type</p><p>`+CancerType +`</p>
            </div>
            <hr>
            <div class="checkbox-container">
                <p style="font-weight: bold;">The Seleted Cancer</p><p>`+select_cancer_Value+`</p>
            </div>
            <hr>
            <div class="checkbox-container">
            <p style="font-weight: bold;">The Seleted Stage </p><p>`+select_stage_Value+`</p>
            </div>
            <hr>
            <div class="checkbox-container">
                <p style="font-weight: bold;">High Percentile</p><p>`+High_Percentile_input+`</p>
            </div>
            <hr>
            <div class="checkbox-container">
                <p style="font-weight: bold;">Low Percentile</p><p>`+Low_Percentile_input+`</p>
            </div>
            <hr>
            <div class="checkbox-container">
                <p style="font-weight: bold;">P-Valus Threshold</p><p>`+Pvalue_input+`</p>
            </div>
            <hr>
            </div>
            <table class="table table-striped" id="result_table2"></table>
        </div>`
  
      // 执行 AJAX 请求
      $.ajax({
        type: 'POST',
        url: '/web_tool/cancer_screener_data/',
        data: {
          'cancer_kind': CancerType,
          'select_cancer': select_cancer_Value,
          'select_stage': select_stage_Value,
          'High_Percentile_input': High_Percentile_input,
          'Low_Percentile_input': Low_Percentile_input,
          'Pvalue_input': Pvalue_input,
        },
        success: function(response) {

          // 清除计时器
          clearInterval(timerInterval);//
          // 隐藏 Spinner
          spinnerContainer.style.display = 'none';//
  
          // 更新页面内容
          document.getElementById('result_table').innerHTML = result_table;
          var max_time = response.result_list[0]['max_time']
          // 初始化 DataTable
          $('#result_table2').DataTable({
            searching: true,
            paging: true,
            info: true,
            scrollCollapse: true,
            data: response.result_list,
            columns: [
              { data: 'name', title: "Gene ID" },
              { data: 'logrank_p_value', title: "Gene Sequence" },
              // { data: 'max_time', title: "Numbers" },
              {
                data: 'name',
                title: "view",
                render: function(data, type, row) {
                    // var maxTime = row.max_time;
                  return '<button type="button" onclick="window.open(\'/web_tool/cancer_web/' + data +'/'+High_Percentile_input+'/'+Low_Percentile_input+'/'+ max_time +'/'+select_stage_Value+'\', \'_blank\')" class="btn btn-warning btn-sm">site</button>';
                }
              },
            ],
            destroy: true,
          });
        },
        error: function() {
        },
      });
    });
  });
  






