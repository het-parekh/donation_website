$(document).ready(function(){

// On Page Load
var load = 4
var step = 4
var domain = "http://127.0.0.1:8000/"
display_category('All',null)
/**************************Categories ******************************/


$(".category-title").click(function(){
    $('.category-title').removeClass('category-active')
    $(this).addClass('category-active')

    display_category($(this).text(),null)  
})
$("#id_category").ready(function(){
    get_sub_categories("Books")
})
$("#id_category").click(function(){
    var cat = $( "#id_category option:selected" ).text();
    get_sub_categories(cat)
})

$("#div_id_sub_category").change(function(){
    var category = $( "#id_category option:selected" ).text()
    var cat  = $('#div_id_sub_category [name=sc]:checked').val()
    send_sub_categories(cat,category)
})


//********************FUNCTION DEFINITIONS***************************** */

function get_sub_categories(cat){
    $.ajax({
        url:window.location.href,
        method:"GET",
        data:{checkboxes:cat},
        success: function (data) {{
            $("#div_id_sub_category").empty()
            data = data['sub_categories']
            row =''
            for(i=0;i<data.length;i++){
            row += ("<div class='sc_container'><label class='radio'><input required  name='sc'  type='radio' \
                        value="+data[i]+"><span>"+data[i]+"</span></label></div>")
            }
            $("#div_id_sub_category").text('Sub Category*').append('<br />')
            $("#div_id_sub_category").append(row)
            }
    }
    })
}

function send_sub_categories(cat,category){
    $.ajax({
        url:window.location.href,
        method:"GET",
        data:{cat:cat,category:category},
        success:function(data){
            
        }

    })
}

function display_category(cat,subcats){
    console.log("subcats value: "+subcats)

    if (subcats == ''){
        subcats = null
    }
    $.get(window.location.href,{display_sub_categories:JSON.stringify(subcats), display_category:cat,})
    .done(function(data){
        posts = $.parseJSON(data['posts'])
        category = (data['category'])
        sub_category = (data['sub_category'])
        distance = data['distance']
        console.log(data)
        $('#search-input').val(window.location.href.split("=")[1])
        row = ''
        for(i = 0;i<posts.length;i++){
            var title  = (posts[i].fields.title.length) > 13?$.trim(posts[i].fields.title).substring(0,15).trim(this)+"...":posts[i].fields.title
            var dis = (distance.length != 0)?Math.round(distance[i]).toFixed(2) + ' kms':'Less than 30 kms'
            row += '<div class = "all books single-post">'+
'                                <div class = "post-img">'+
'                                    <img src = "'+ domain + "media/" + posts[i].fields.main_image +'" alt = "post_image">'+
'                                    <span class = "category-name">'+ category[i] +'</span>'+
'                                </div>'+
'                                <div class = "post-content" >'+
'                                    <div class = "post-content-top">'+
'                                        <span><i class = "fas fa-calendar"></i>'+ posts[i].fields.date +'</span>'+
'                                        <span class = "float-right"><i class = "fas fa-calendar"></i>'+ dis +'</span>'+
'                                        '+
'                                    </div>'+
'                                    <h2>'+ title +'<span  class=\'badge badge-dark float-right\' >'+ sub_category[i] +'</span></h2>'+
'                                </div>'+
'                                <button value="'+ posts[i].fields.slug +'" id="post_detail_btn" type = "button" class = "readbtn btn-outline-dark">Get Now</button>'+
'                            </div>';
	
        }
        $("#post_container_id").empty()
        $("#post_container_id").append(row)
        if ($("#loadmore").length == 0){
            $("#post_collect_id").append("<br /><center><button id='loadmore'>Load More</button></center>;")
        }
        loadMore()
        
    })
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/
$("#post_collect_id").on('click','#post_detail_btn',function(){
    location.href = domain+"post_detail/"+$(this).val()
})
/******************Sub Categories********************************* */
$(".category-title").click(function(){
    switch_category($(this).text())
    $("#hr").remove()
    load = step
    category = $(this).text()
})
$("#sub_category_id").on('click','.sub_category',function(){ 
    var arr = []

    $(this).toggleClass("sub_category-clicked")
    $(".sub_category-clicked").each(function(){
        arr.push($(this).text())
    })
    category = $(".category-active").text()
    display_category(category,arr)
    
})

$("#post_collect_id").on("click",'#loadmore',function(){
    
    load += step
    loadMore()
})
//********************FUNCTION DEFINITIONS***************************** */

function switch_category(category){
    $.ajax({
        url:window.location.href,
        method:"GET",
        data:{category:category},
        success:function(data){
            data = data['sub_categories']
            if (data == "ALL"){
                $("#sub_category_id").empty()
                return
            }
            row = ''
            
            for(i=0;i<data.length;i++){
                row += "<button class='sub_category'>"+(data[i])+"</button>"
            }
            $("#sub_category_id").empty()
            $("#sub_category_id").append(row)
            $("<hr class='separator separator--line' id='hr' /> ").insertAfter("#sub_category_id")
        }
    })
}

function loadMore(){
    $(".single-post").slice(0,).hide()
    $("#loadmore").hide()
    if($(".single-post").length > load){
            $("#post_collect_id").show()
            $(".single-post").slice(0,load-step).show()
            $(".single-post").slice(load-step,load).slideDown('fast')
            $("#loadmore").show() 
        }else{
        x = $(".single-post").length
        if (x <= step){
            $(".single-post").slice(0,x).slideDown('fast')
        }
        else{
            $(".single-post").slice(0,load-step).show()
            $(".single-post").slice(load-step,x).slideDown('fast')
        }
    }
    
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/


/*******************************************************************************************
 *                                 LOCATION 
 ********************************************************************************************/

 $(".location_inner > i").click(function(){
    send_location()
 })

/******************************************************************************************* */

/*******************************************************************************************
 *                                 SEND LOCATION
 ********************************************************************************************/

if(navigator.geolocation){
    function getPosition() {
        return new Promise((res, rej) => {
            navigator.geolocation.getCurrentPosition(res, rej,{timeout:10000});
        });
    }  
}
else{
    alert("Your Browser doesn't support navigation. Getting the closest possible location...")
}
send_location()

function send_location() {
    getPosition().then((position)=>{
        $(".location_validation").html('<span style="color:green"><i class="fa fa-check-circle"></i>  Location Successfully Fetched... </span>')
        $.get(window.location.href,{'geo[]':[position.coords.latitude,position.coords.longitude]})
        .done(function(data){
            if (data['address']){
                data = data['address']
                
                $("#id_state").val(data[4])
                $("#id_city").val(data[2])
                $("#id_pincode").val(data[3])
            }
        })
}).catch((error)=>{
    if(error.message == 'User denied Geolocation'){
        $(".location_validation").html('<span style="color:red"><i class="fa fa-warning"></i>   Location Services blocked by the user or timed out. Getting the closest possible location... </span>')
        $(".location_inner input").val("Approximate Location")
        $.get(window.location.href,{'geo_denied':'geo_denied'})
        .done(function(data){
            if (data['address']){
                data = data['address']
                $("#id_state").val(data[4])
                $("#id_city").val(data[2])
                $("#id_pincode").val(data[3])
            }
        })
        } 
    })
}
/*********************************************************************************************** */










})