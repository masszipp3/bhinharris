$(document).ready(function(){
 validation()
})

function validation(){
    var bht = $('#btnradio1d')
    var other = $('#btnradio3d')
    var name = $('#name').val()==''
    var phone = $('#phone').val()==''
    var house = $('#house').val()==''
    var city = $('#city').val()==''
    var street = $('#address').val()==''
    var province = $('#province').val()==''
    var district = $('#district').val()==''
    var postalcode = $('#postalcode').val()==''
    var landmark = $('#Landmark').val()==''

    if(bht.is(':checked')){
        $('#name').attr('required',true)
        $('#phone').attr('required',true)
        $('#house').attr('required',true)
        $('#city').attr('required',true)
        if(name || phone || house || city){
            // $('#submitbutton').removeAttr('data-bs-dismiss')
            $('#addressdiv').slideDown()
            $('#deliverydiv').slideUp()
            $('#deliveryadd').html('No address added')

            return true
        }
        else{
            // $('#submitbutton').attr('data-bs-dismiss','offcanvas')
            $('#addressdiv').slideUp()
            $('#deliverydiv').slideDown()
            return false
        }



        
    }
    if(other.is(':checked')){
        $('#name').attr('required',true)
        $('#phone').attr('required',true)
        $('#house').attr('required',true)
        $('#city').attr('required',true)
        if(name || phone || house || city || street || province || district || postalcode){
            // $('#submitbutton').removeAttr('data-bs-dismiss')
            $('#addressdiv').slideDown()
            $('#deliverydiv').slideUp()
            $('#deliveryadd').html('No address added')
            return true
        }
        else{
            // $('#submitbutton').attr('data-bs-dismiss','offcanvas')
            $('#addressdiv').slideUp()
            $('#deliverydiv').slideDown()
            return false
        }



        
    }
}