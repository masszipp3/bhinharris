$(document).ready(function () {

    $('#title').on('input', function () {
        var title = $(this).val();
        var slug = '';

        // Convert title to lowercase and replace spaces with dashes
        slug = title.toLowerCase().replace(/\s+/g, '-');

        // Remove special characters except dashes
        slug = slug.replace(/[^\w-]+/g, '');

        // Update the slug field with the generated value
        $('#slug').val(slug);
    });
});



$(document).ready(function () {
  var formslug=0
  var formid=0
    var editProductUrl = '{% url "smsuser:productdetails" 0 %}';
        $.ajaxSetup({
          headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
          }
        })
    $('#title').on('input', function () {
        var title = $(this).val();
        var slug = '';

        // Convert title to lowercase and replace spaces with dashes
        slug = title.toLowerCase().replace(/\s+/g, '-');

        // Remove special characters except dashes
        slug = slug.replace(/[^\w-]+/g, '');

        // Update the slug field with the generated value
        $('#slug').val(slug);
    });

    $('#catid').on('input',function(){
      console.log('hhh')
      catid=$(this).val()
      slug=$('#slug').val()
      url=$('#caturl').data('url')
      console.log(url)
      $.ajax({

       type:'POST',
       url:url,
       data:{
        'catid':catid,
       },
       success:function(response){
        if (response.msg=='Available'){
          $('#catidcheck').removeClass('text-danger fa-close')
          $('#catidcheck').addClass('text-sucess fa-check')
          $('#catidcheck').html('Available')
          $('#catidcheck').show()
          formid=1
          

        }
        else{
          $('#catidcheck').removeClass('text-sucess fa-check')
          $('#catidcheck').addClass('text-danger fa-close')
          $('#catidcheck').html('Catagory ID Already Exists')
          $('#catidcheck').show()
          formid=0
        }
        if(catid==''){
          formid=0
          $('#catidcheck').hide()
        }
        
       },
       error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }

      })

  
    })

    $('#title').on('input',function(){
      console.log('hhh')
      slug=$('#slug').val()
      url=$('#caturl').data('url')
      console.log(url)
      $.ajax({

       type:'POST',
       url:url,
       data:{
        'slug':slug,
       },
       success:function(response){
        console.log(response)
        if (response.msg=='Available'){
          $('#slugcheck').removeClass('text-danger fa-close')
          $('#slugcheck').addClass('text-sucess fa-check')
          $('#slugcheck').html('Available')
          $('#slugcheck').show()
          formslug=1
          

        }
        else{
          $('#slugcheck').removeClass('text-sucess fa-check')
          $('#slugcheck').addClass('text-danger fa-close')
          $('#slugcheck').html('Slug Already Exists')
          $('#slugcheck').show()
          formslug=0
        }
        if(slug==''){
          formslug=0
          $('#slugcheck').hide()
        }
       },
       error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }

      })


  
    })

    $("#catagoryform").submit(function(event) {
      if(formslug == 0 || formid == 0){
        console.log(formslug,formid)
        event.preventDefault(); 
      }
        

    })
    
    $('#productsearch').on('input',function(){
        search_data=$(this).val();
        
        url=$('#myform').data('url')
        $.ajax({
            type: 'POST',
            url: url,
            data: {
              'keyword': search_data
            },
            success: function (response) {
              data = response.searchdata
              console.log(response.searchdata)
              $('#searchdetails').show()
              $('#searchdetails').empty()
              if(search_data != ''){
                for(i=0;i<data.length;i++){
                    var link=$('<a></a>')
                        var img=$('<img>')
                    var url='/media/'+data[i].product_image
                    var productUrl ='/smsuser/' + data[i].id + '/productdetails';
                   
                    img.attr('src', url).attr('height','35px').attr('width','35px')
                    var searchResultDiv = $('<div></div>');
                    searchResultDiv.addClass('searchresult');
                    var span=$('<span></span>')
                    searchResultDiv.append(span)
                    
                    link.attr('href', productUrl);

                   
                    
                    span.html(data[i].Product_ID+':'+data[i].Product_name)
                    searchResultDiv.append(img)
                    link.append(searchResultDiv)
                    $('#searchdetails').append(link)
                   console.log(data[i].brand)
                   
    
                  }

              }
              else{
                $('#searchdetails').hide()

              }
              
              
              
              
            //   console.log(total)
            //   console.log(count)
      
            //   addButton.hide();
            //   productCountDiv.removeClass("none").show();
            //   productCountInput.val("1");
              // $('#hoi').empty();
              // $('#hoi').append($('<option>').text('Select a Staff').attr('value', ''));
              // for (d in data) {
              //     console.log(d)
              //     $('#hoi').append($('<option>').text(data[d].name).attr('value',data[d].id));
              // }
            },
            error: function (xhr, status, error) {
              console.error(xhr.responseText);
            }
          });

    })

    $('#proid').on('input',function(){
      console.log('hhh')
      proid=$(this).val()
      slug=$('#slug').val()
      url=$('#prourl').data('url')
      console.log(url)
      $.ajax({

       type:'POST',
       url:url,
       data:{
        'proid':proid,
       },
       success:function(response){
        if (response.msg=='Available'){
          $('#catidcheck').removeClass('text-danger fa-close')
          $('#catidcheck').addClass('text-sucess fa-check')
          $('#catidcheck').html('Available')
          $('#catidcheck').show()
          formid=1
          

        }
        else{
          $('#catidcheck').removeClass('text-sucess fa-check')
          $('#catidcheck').addClass('text-danger fa-close')
          $('#catidcheck').html('Product ID Already Exists')
          $('#catidcheck').show()
          formid=0
        }
        if(proid==''){
          formid=0
          $('#catidcheck').hide()
        }
        
       },
       error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }

      })

  
    })

    $('#title').on('input',function(){
      console.log('hhh')
      slug=$('#slug').val()
      url=$('#prourl').data('url')
      console.log(url)
      $.ajax({

       type:'POST',
       url:url,
       data:{
        'slug':slug,
       },
       success:function(response){
        console.log(response)
        if (response.msg=='Available'){
          $('#slugcheck').removeClass('text-danger fa-close')
          $('#slugcheck').addClass('text-sucess fa-check')
          $('#slugcheck').html('Available')
          $('#slugcheck').show()
          formslug=1
          

        }
        else{
          $('#slugcheck').removeClass('text-sucess fa-check')
          $('#slugcheck').addClass('text-danger fa-close')
          $('#slugcheck').html('Slug Already Exists')
          $('#slugcheck').show()
          formslug=0
        }
        if(slug==''){
          formslug=0
          $('#slugcheck').hide()
        }
       },
       error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }

      })


  
    })

    $("#productform").submit(function(event) {
      if(formslug == 0 || formid == 0){
        console.log(formslug,formid)
        event.preventDefault(); 
      }
        

    })

    $('#price').on('input',function(){
      price=$('#price').val();
      discount=$('#discount').val()
      total=(parseFloat(price)-((parseFloat(price)*parseInt(discount))/100)).toFixed(1)
      $('#finalprice').val(total)

    })

    $('#discount').on('input',function(){
      price=$('#price').val();
      discount=$('#discount').val()
      total=(parseFloat(price)-((parseFloat(price)*parseInt(discount))/100)).toFixed(1)
      $('#finalprice').val(total)

    })

    $('#ordersearch').on('input',function(){
        search_data=$(this).val();
        console.log(search_data)
        
        url=$('#myorderform').data('url')
        $.ajax({
            type: 'POST',
            url: url,
            data: {
              'keyword': search_data
            },
            success: function (response) {
              data = response.searchdata
              console.log(response.searchdata)
              $('#searchdetails').show()
              $('#searchdetails').empty()
              if(search_data != ''){
                for(i=0;i<data.length;i++){
                    console.log(data[i].OrderId)
                    var link=$('<a></a>')
                    var productUrl ='/smsuser/' + data[i].OrderId + '/orderdetails';
                   
                    var searchResultDiv = $('<div></div>');
                    searchResultDiv.addClass('searchresult');
                    var span=$('<span></span>')
                    searchResultDiv.append(span)
                    
                    link.attr('href', productUrl);

                   
                    
                    span.html(data[i].OrderId+':'+data[i].user__customer_name)
                    link.append(searchResultDiv)
                    $('#searchdetails').append(link)
                   console.log(data[i].brand)
                   
    
                  }

              }
              else{
                $('#searchdetails').hide()

              }
              
            },
            error: function (xhr, status, error) {
              console.error(xhr.responseText);
            }
          });

    })
});


function confirmDelete(event) {
    event.preventDefault();
    if (confirm("Are you sure you want to delete this item?")) {
        return true
    }
    else{
        return false
    }
}