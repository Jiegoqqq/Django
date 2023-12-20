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
        var select_conditon2 = document.getElementById('select_conditon2');
        var select_conditon2_Value = select_conditon2.value;
        var select_conditon1 = document.getElementById('select_conditon1');
        var select_conditon1_Value = select_conditon1.value;
        var select_type1 = document.getElementById('select_type1');
        var select_type1_Value = select_type1.value;
        var type1_input = $("#type1_input").val();
        var select_test = document.getElementById('select_test');
        var select_test_Value = select_test.value;
        var select_type2 = document.getElementById('select_type2');
        var select_type2_Value = select_type2.value;
        var qvalue_input = $("#qvalue_input").val();
    
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
                  <p style="font-weight: bold;"> Seleted Condition 2 </p><p>`+select_conditon2_Value+`</p>
              </div>
              <hr>
              <div class="checkbox-container">
              <p style="font-weight: bold;"> Seleted Condition 1 </p><p>`+select_conditon1_Value+`</p>
              </div>
              <hr>
              <div class="checkbox-container">
                  <p style="font-weight: bold;"> Fold Change </p><p>`+ type1_input +`</p>
              </div>
              <hr>
              <div class="checkbox-container">
                  <p style="font-weight: bold;"> Selected Test </p><p>`+select_test_Value+`</p>
              </div>
              <hr>
              <div class="checkbox-container">
                  <p style="font-weight: bold;"> Q-Valus Threshold </p><p>`+qvalue_input+`</p>
              </div>
              <hr>
              </div>
              <table class="table table-striped" id="table1"></table>
          </div>`
        $.ajax({
            type: 'POST',
            url: '/web_tool/liver_screener_data/',
            data: {
              'cancer_kind': CancerType,
              'select_cancer': select_cancer_Value,
              'select_conditon2_Value': select_conditon2_Value,
              'select_conditon1_Value': select_conditon1_Value,
              'select_type1_Value': select_type1_Value,
              'type1_input': type1_input,
              'select_test_Value': select_test_Value,
              'select_type2_Value': select_type2_Value,
              'qvalue_input':qvalue_input,
            },
            success: function(response) {
                // 清除计时器
                clearInterval(timerInterval);//
                // 隐藏 Spinner
                spinnerContainer.style.display = 'none';//
                document.getElementById('result_table').innerHTML = result_table;
                $('#table1').DataTable({
                    searching: true,
                    paging: true,
                    info: true,
                    scrollCollapse: true,
                    data: response.table_list,
                    dom: 'Bfrtip',  // 指定要使用的功能按鈕
                    buttons: [
                        'csv', // 指定導出的格式
                    ],
                    columns: [
                        { data: 'gene', title: "Gene" },
                        { data: 'value_2', title: "Condition 2" },
                        { data: 'value_1', title:"Condition 1"},
                        { data: 'fold_change', title:"Fold change"},
                        { data: 'q_value', title: "Q value" },
                    ],
                    /*auto refrash*/
                    destroy:true,
                });
            },
            error: function() {
            },
        })
    })




})