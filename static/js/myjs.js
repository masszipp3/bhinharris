$(document).ready(function () {
  $('#btnradio3d').click(function () {
    $('#Landmark').show()
    $('#address').show()

    $('#district').show()
    $('#province').show()
    $('#postalcode').show()
    $('#appt').hide()

    console.log('hh')
  })
  $('#btnradio1d').click(function () {
    $('#Landmark').hide()
    $('#address').hide()
    $('#district').hide()
    $('#province').hide()
    $('#postalcode').hide()
    $('#appt').show()

  })

})

$(document).ready(function () {
  
  divheight()
  var query = window.location.search;
  var urlParams = new URLSearchParams(query);
  var categoryValue = urlParams.get('catagory');
      console.log(categoryValue);

  $.ajaxSetup({
    headers: {
      "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
    }
  })
  $('#goback').click(function () {
    window.history.back();
  })

  $('#searchs').on('input', function () {
    url = $(this).data('url')
    console.log(url)
    searchlist = []
    var query = $('#searchs').val()
    console.log(query)

    console.log('hh')
    if (query.length > 1) {

      $.ajax({
        type: 'POST',
        url: url,
        data: { 'query': query },
        success: function (response) {
          $('#searchdiv').empty()
          var data = response.data
          for (var i = 0; i < data.length; i++) {
            searchlist.push(data[i])
          }

          const matchingsearch = searchlist.filter((searchdata) => searchdata.toLowerCase().includes((query).toLowerCase()))
          console.log(matchingsearch)

          for (var i = 0; i <= matchingsearch.length; i++) {
            var h6 = $('<h6 class="px-3 pb-3 m-0 ms-5 searchresult"></h6>')
            var searchurltag = $('<a></a>')
            searchurl = url + '?query=' + matchingsearch[i]
            searchurltag.attr('href', searchurl)
            h6.html(matchingsearch[i])
            searchurltag.append(h6)
            $('#searchdiv').append(searchurltag)
          }
          var h6 = $('<h6 class="px-3 pb-3 m-0 ms-5 searchresult border-bottom"></h6>')
          var searchurltag = $('<a></a>')
          searchurl = url + '?query=' + query
          searchurltag.attr('href', searchurl)
          h6.html('See all results for <b>' + query + '</b>')
          searchurltag.append(h6)
          $('#searchdiv').append(searchurltag)
        }

      })
    }
    else {
      $('#searchdiv').empty()
    }
  })

  function updateProductCountDiv(productCountDiv) {
    var productCountInput = productCountDiv.find("input");
    var addButton = productCountDiv.siblings(".proadd");
    var defaultCount = parseInt(productCountInput.val());

    if (defaultCount > 0) {
      addButton.hide();
      productCountDiv.removeClass('none');
      productCountDiv.show();
    } else {
      addButton.show();
      productCountDiv.hide();
    }
  }

  $(".productcountdiv").each(function () {


    updateProductCountDiv($(this));
  });


  $(document).on("click", ".proadd", function () {
    console.log('dd')
    var productContainer = $(this).closest(".card-footer");
    var url = productContainer.data('url')
    console.log(productContainer)
    var productid = productContainer.find(".checkid").attr("id");
    console.log(productid)
    var addButton = $(this);
    var productCountDiv = productContainer.find(".productcountdiv");
    var productCountInput = productCountDiv.find("input");

    $.ajax({
      type: 'POST',
      url: url,
      data: {
        'productid': productid
      },
      success: function (response) {
        data = response.data
        total = 'Rs ' + response.total
        count = response.count + ' items in cart'
        $('#counts').html(count)
        $('#total').html(total)


        console.log(total)
        console.log(count)

        addButton.hide();
        productCountDiv.removeClass("none").show();
        productCountInput.val("1");
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

  });
  $(document).on("click", ".minus", function () {
    var productContainer = $(this).closest(".card-footer");
    var addButton = productContainer.find(".proadd");
    var productCountDiv = productContainer.find(".productcountdiv");
    var productCountInput = productCountDiv.find("input");
    var productid = productCountInput.attr('ppid')
    url = $("#minusurl").data('url')
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        'productid': productid
      },
      success: function (response) {
        data = response.data
        total = 'Rs ' + response.total
        subtotal = 'OMR ' + response.subt
        count = response.count + ' items in cart'
        $('#counts').html(count)
        $('#total').html(total)
        var currentCount = parseInt(productCountInput.val());
        console.log(productCountInput.val())
        if (currentCount > 0) {
          productCountInput.val(currentCount - 1);
          console.log(productCountInput.val())
        }
        if (productCountInput.val() < 1) {
          addButton.show();
          productCountDiv.addClass("none")
        }

        // console.log(data)
        // addButton.hide();
        // productCountDiv.removeClass("none").show();
        // productCountInput.val("1");
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




  });
  var page = 2;
  var value=$('#nextpage').val()
  console.log(value)
  if(value=='yes'){
    var nextpage = true // Initial page number
  }
  else{
    var nextpage = false   // Initial page number
  }
  

  // Function to load the next page of products
  function loadNextPage() {
    url = $('#productsdiv').data('url')
    $.ajax({
      type: 'GET',
      url: url,
      data: { 'page': page,'catagory':categoryValue },
      success: function (response) {


        var data = response.products
        var quantities = response.quantities
        console.log(quantities)
        console.log(data)
        var counter = 1
        prourl = $('#addpro').data('url')
        prominus = $('#minuspro').data('url')
        for (i = 0; i < data.length; i++) {
          console.log('next', nextpage)
          if (nextpage == true) {
            console.log(typeof(quantities))
            if(quantities.length!=0){
              var product = data[i];
            for (key in quantities) {
              if (product.id == key) {
                productquantity = quantities[key]
                break;
              }
              else {
                   productquantity = 0
              }

            }
            }
            else{
              var productquantity=0
            }
            
           
            
            var productItem = `
          <div class="col-6 bordr">
            <div class="card bg-transparent border-0 p-2 h-100">
              <div class="bg-success position-absolute top-0 text-white osahan-badge text-center">
                <b>BHT</b><br>Assured
              </div>
              <a href="product/${product.slug}">
                <img src="${product.img}" alt="" class="img-fluid w-75 d-block mx-auto">
              </a>
              <div class="card-body p-0 mb-3">
                <small class="text-muted">${product.brand}</small>
                <p class="card-title fw-bold mb-0">${product.name}</p>
              </div>
              <div class="card-footer bg-transparent border-0 d-flex align-items-end justify-content-between p-0"  id="addurl" data-url="${prourl}">
                <div class="cartdet">
                  <p id="${product.id}" class="checkid text-muted mb-1">${product.minvalue}${product.unit}</p>
                  <del class="text-muted small">₹${product.initialprice}</del>
                  <p class="fw-bold m-0">₹${product.price}</p>
                </div>
                <button class="btn proadd btn-outline-success btn-sm border-dark-subtle fw-bold rounded-3 shadow-sm px-3">ADD</button>
                <div style="display: none !important;" class="productcountdiv none osahan-count d-flex align-items-center justify-content-between border border-dark-subtle rounded-pill h6 m-0 p-1">
                  <span class="text-muted minus d-flex"><i class="icofont-minus-circle"></i></span>
                  <input type="text" value="${productquantity}" ppid="${product.id}" disabled id="productcount01" class="lh-sm small text-black text-center box border-0">
                  <span id="minusurl" data-url="${prominus}" class="text-muted plus d-flex"><i class="icofont-plus-circle"></i></span>
                </div>
              </div>
            </div>
          </div>
        `;
            var productItem2 = `
        <div class="col-6 bordr border-end">
          <div class="card bg-transparent border-0 p-2 h-100">
            <div class="bg-success position-absolute top-0 text-white osahan-badge text-center">
              <b>BHT</b><br>Assured
            </div>
            <a href="product/${product.slug}">
              <img src="${product.img}" alt="" class="img-fluid w-75 d-block mx-auto">
            </a>
            <div class="card-body p-0 mb-3">
              <small class="text-muted">${product.brand}</small>
              <p class="card-title fw-bold mb-0">${product.name}</p>
            </div>
            <div class="card-footer bg-transparent border-0 d-flex align-items-end justify-content-between p-0"  id="addurl" data-url="${prourl}">
              <div class="cartdet">
                <p id="${product.id}" class="checkid text-muted mb-1">${product.minvalue}${product.unit}</p>
                <del class="text-muted small">₹${product.price}</del>
                <p class="fw-bold m-0">₹${product.price}</p>
              </div>
              <button class="btn proadd btn-outline-success btn-sm border-dark-subtle fw-bold rounded-3 shadow-sm px-3">ADD</button>
              <div style="display: none !important;" class="productcountdiv none osahan-count d-flex align-items-center justify-content-between border border-dark-subtle rounded-pill h6 m-0 p-1">
                <span class="text-muted minus d-flex"><i class="icofont-minus-circle"></i></span>
                <input type="text" value="${productquantity}" ppid="${product.id}" disabled id="productcount01" class="lh-sm small text-black text-center box border-0">
                <span id="minusurl" data-url="${prominus}" class="text-muted plus d-flex"><i class="icofont-plus-circle"></i></span>
              </div>
            </div>
          </div>
        </div>
      `;
            if (counter % 2 == 0) {
              $('#productsdiv').append(productItem2);
              console.log('res', response.has_next_page)
              nextpage = response.has_next_page
              counter++

            }
            else {
              $('#productsdiv').append(productItem);
              console.log('res', response.has_next_page)
              
              counter++
            }
            page++;
            $('#loader').hide()

            var productCountDiv = $('#productsdiv').find('.productcountdiv').last();
            updateProductCountDiv(productCountDiv);


          }

        }
        nextpage=response.has_next_page



        // Increment the page number for the next request
        
        console.log(page)
        // $('#loader').hide()
      },
      error: function (xhr, status, error) {
        console.log(error); // Handle error, if any
      }
    });
    divheight()
  }

  // Load the initial page of products

  function isScrollAtBottom() {
    var scrollContainer = $('#scroll');
    var scrollHeight = scrollContainer.prop('scrollHeight');
    var scrollTop = scrollContainer.scrollTop();
    var containerHeight = scrollContainer.height()+100
    console.log('containerHeight',containerHeight,'scrollTop',scrollTop,'scrollHeight',scrollHeight)
    return scrollTop + containerHeight >= scrollHeight;

  }


  // Load next page when user scrolls to the bottom of the page
  $('#scroll').scroll(function () {
    

    if (isScrollAtBottom()) {
      if(nextpage==true){
        $('#loader').show()

        loadNextPage();
        

      }
      
      // Load the next page
      
    

      // i=0
      // while(i<1){
      //   i=0
      // }


    }




  });
  function divheight(){
    var vhInPixels = window.innerHeight * 0.01;
    var vhInPixels = window.innerHeight * 0.01;
    $("#scroll").height(100 * vhInPixels);
    console.log('height')
   
  }


  $(".plus").click(function () {
    var productContainer = $(this).closest(".card-footer");
    var productCountInput = productContainer.find("input");
    var productid = productCountInput.attr('ppid')
    url = $("#addurl").data('url')

    console.log(productCountInput.val())
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        'productid': productid
      },
      success: function (response) {
        data = response.data
        total = 'Rs ' + response.total
        count = response.count + ' items in cart'
        $('#counts').html(count)
        $('#total').html(total)

        console.log(count)
        console.log(total)
        var currentCount = parseInt(productCountInput.val());
        productCountInput.val(currentCount + 1);

        // console.log(data)
        // addButton.hide();
        // productCountDiv.removeClass("none").show();
        // productCountInput.val("1");
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






  });

  if ($('#quandity').val() >= 1) {
    $('#none').hide()
    $('#block').show()

  }

  $("#addtocart").click(function () {
    var quaditydiv = $('#quandity')
    var quantity = quaditydiv.val()
    var productid = quaditydiv.attr('ppid')
    url = quaditydiv.data('url')

    $.ajax({
      type: 'GET',
      url: url,
      data: {
        'productid': productid,
        'quantity': quantity
      },
      success: function (response) {
        data = response.data
        console.log(data)
        $('#quandity').val(response.quantity)
        $('#none').hide()
        $('#block').show()



        // console.log(data)
        // addButton.hide();
        // productCountDiv.removeClass("none").show();
        // productCountInput.val("1");
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








  });

  $(".addcoupon").click(function () {
    var couponcode = $(this).attr('ppid')
    var couponid = $(this).attr('id')
    var discount = $('#discountt')
    var url = $('#applycouponurl').data('url')


    $.ajax({
      type: 'POST',
      url: url,
      data: {
        'couponid': couponid,
      },
      success: function (response) {
        data = response.data
        console.log(data)

        discountamount = response.discount
        discount.html('OMR '+discountamount)
        $('#finaldiscount').html('- OMR ' + discountamount)
        // $('#grandtotal').html('OMR '+response.total)
        // $('#finaltotal').html('OMR '+response.total)
        var total = parseFloat(response.finaltotal)
        // var vat = total * 0.05
        // var total = total + vat
        console.log(total)
        $('#downtotal').html('OMR ' + total.toFixed(2))
        $('#subtotals').html('OMR ' + total.toFixed(2))
        // $('#vat').html('OMR ' + vat.toFixed(2))
        $('#grandtotal').html('OMR '+response.total)
        $('#finaltotal').html('OMR '+response.total)
        // $('#finalvat').html('OMR '+vat.toFixed(2))
        $('#finalamount').html('OMR '+total)
        var discounts=response.total-response.finaltotal
        console.log(discounts)
        $('#finaldiscount').html('OMR '+discounts.toFixed(2))
        $('#couponss').html(couponcode + ' applied').css('color', 'green')
        var couponIdInput = $('<input>').attr({
          type: 'hidden',
          name: 'coupon_id',
          value: couponid
        })
        $('#deliverform').append(couponIdInput);






        // console.log(data)
        // addButton.hide();
        // productCountDiv.removeClass("none").show();
        // productCountInput.val("1");
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


  });

  $('#cancel').click(function(){
    $(this).slideUp(100)
    // $('#confirm').show()
    $('#confirm').slideDown(500)
    // $(this).slideDown()
  })

  $('#confirm').click(function(){
    $(this).slideUp(100)
    // $('#confirm').show()
    $('#cancel').slideDown(500)
    // $(this).slideDown()
  })


  $("#submitbutton").click(function () {
    
    // var bht = $('#btnradio1d')
    // var other = $('#btnradio3d')
    // var name = $('#name').val()
    // var phone = $('#phone').val()
    // var house = $('#house').val()
    // var city = $('#city').val()
    // var street = $('#address').val()
    // var province = $('#province').val()
    // var district = $('#district').val()
    // var postalcode = $('#postalcode').val()
    // var landmark = $('#Landmark').val()
    // if(bht.is(':checked')){
    //   if(name=='')
    // }
    if(! validation()){
      
      deliveryaddress()

    }
    

  });



  $('#dlater').click(function () {
    $('#delivery').show()
  })

  $('#dnow').click(function () {
    $('#delivery').hide()
  })

});

function deliveryaddress () {
  var formdata = $('#myform').serialize()
  var url = $('#myform').data('url')
  console.log(formdata)


  $.ajax({
    type: 'POST',
    url: url,
    data: formdata,
    success: function (response) {
      data = response.data
      console.log(data)
      address = response.data.customer_name + ', ' + response.data.House + ', ' + response.data.City+', '+ response.data.Mobile
        $('#deliveryadd').html(address)
        

    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    }
  });

}