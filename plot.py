def plot(list,target,regulator,name):
    top = 0
    bottom = 0 
    ans = ''
    for i in range(0,len(list)):
        top = list[i][target]
        bottom = list[i][regulator]
        ans_u = ''
        ans_b = ''
        ans_u += '<span style="white-space:nowrap"> 5\' '
        for j in range(0,len(top)):
            #C
            if top[j] == 'C' and bottom[j] == 'A':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'C' and bottom[j] == 'U':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'C' and bottom[j] == 'T':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="m">' +'U'+'</span class="y">'
            elif top[j] == 'C' and bottom[j] == 'C':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'        
            elif top[j] == 'C' and bottom[j] == 'G':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'  
            #G   
            elif top[j] == 'G' and bottom[j] == 'U':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="b">' +bottom[j]+ '</span class="y">'
            elif top[j] == 'G' and bottom[j] == 'A':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'G' and bottom[j] == 'T':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'     
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'G' and bottom[j] == 'G':    
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'       
            elif top[j] == 'G' and bottom[j] == 'C':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'  
            #A
            elif top[j] == 'A' and bottom[j] == 'C':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+ '</span class="y">'
            elif top[j] == 'A' and bottom[j] == 'G':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'A' and bottom[j] == 'T':  
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'   
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'
            elif top[j] == 'A' and bottom[j] == 'A': 
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'    
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'           
            elif top[j] == 'A' and bottom[j] == 'U':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'  
            #U
            elif top[j] == 'U' and bottom[j] == 'C':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+ '</span class="y">'
            elif top[j] == 'U' and bottom[j] == 'G':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="b">' +bottom[j]+'</span class="y">'
            elif top[j] == 'U' and bottom[j] == 'T': 
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'     
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'U' and bottom[j] == 'U':   
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'           
            elif top[j] == 'U' and bottom[j] == 'A':
                ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'  
            #T
            elif top[j] == 'T' and bottom[j] == 'C':
                ans_u += '<span class="y" >' +'U'+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+ '</span class="y">'
            elif top[j] == 'T' and bottom[j] == 'G':
                ans_u += '<span class="y" >' +'U'+'</span class="y">'  
                ans_b += '<span class="y" id="b">' +bottom[j]+'</span class="y">'
            elif top[j] == 'T' and bottom[j] == 'U':    
                ans_u += '<span class="y" >' +'U'+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +bottom[j]+'</span class="y">'
            elif top[j] == 'T' and bottom[j] == 'A':
                ans_u += '<span class="y" >' +'U'+'</span class="y">'  
                ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'  
            elif top[j] == 'T' and bottom[j] == 'T':
                ans_u += '<span class="y" >' +'U'+'</span class="y">'  
                ans_b += '<span class="y" id="y">' +'U'+'</span class="y">'         
            #-
            elif top[j] == '-' :
                if bottom[j] == 'T':
                    ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                    ans_b += '<span class="y" id="g">' +'U'+ '</span class="y">'
                else:
                    ans_u += '<span class="y" >' +top[j]+'</span class="y">'  
                    ans_b += '<span class="y" id="g">' +bottom[j]+ '</span class="y">'
            elif bottom[j] == '-':
                if top[j] == 'T':
                    ans_u += '<span class="y" id="g">' + 'U' + '</span class="y">'
                    ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'   
                else:
                    ans_u += '<span class="y" id="g">' + top[j]+ '</span class="y">'
                    ans_b += '<span class="y" >' +bottom[j]+'</span class="y">'                        
        ans_u += ' 3\'  <br> 3\' '
        ans_b +=  ' 5\' <br> '
        ans = ans_u+ans_b
        list[i][name] = ans
    return list