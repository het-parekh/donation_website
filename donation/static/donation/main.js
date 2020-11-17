$(document).ready(function(){

// On Page Load
var load = 4
var step = 4
display_category('All',null)
/**************************Categories ******************************/
if(navigator.geolocation){
    var n = navigator.geolocation.getCurrentPosition(showPosition);
    console.log(n)
}

function showPosition(position) {
      console.log("Latitude: " + position.coords.latitude + 
      "<br>Longitude: " + position.coords.longitude); 
     }
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
    $.get(window.location.href,{display_category:cat,display_sub_categories:JSON.stringify(subcats)})
    .done(function(data){
        posts = $.parseJSON(data['posts'])
        categogy = (data['category'])
        image = (data['image'])
        sub_category = (data['sub_category'])
        console.log(categogy)
        console.log(image)
        row = ''
        for(i = 0;i<posts.length;i++){
            var title  = (posts[i].fields.title.length) > 13?$.trim(posts[i].fields.title).substring(0,15).trim(this)+"...":posts[i].fields.title
            row += '<div class = "all books single-post">'+
'                                <div class = "post-img">'+
'                                    <img src = "'+ window.location.href + image[i].substring(3,image[i].length-2)+'" alt = "post_image">'+
'                                    <span class = "category-name">'+ categogy[i] +'</span>'+
'                                </div>'+
'                                <div class = "post-content" >'+
'                                    <div class = "post-content-top">'+
'                                        <span><i class = "fas fa-calendar"></i>'+ posts[i].fields.date +'</span>'+
'                                        '+
'                                    </div>'+
'                                    <h2>'+ title +'<span  class=\'badge badge-dark float-right\' >'+ sub_category[i] +'</span></h2>'+
'                                </div>'+
'                                <button type = "button" class = "read-btn">Get Now</button>'+
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

/******************Sub Categories********************************* */
$(".category-title").click(function(){
    switch_category($(this).text())
    $("#hr").remove()
    category = $(this).text()
})
$("#sub_category_id").on('click','.sub_category',function(){ 
    var arr = []
    $(this).toggleClass("sub_category-clicked")
    $(".sub_category-clicked").each(function(){
        arr.push($(this).text())
    })
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
        $(".single-post").slice(0,x-step).show()
        $(".single-post").slice(x-step,x).slideDown('fast')
    }
    
}

/*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx*/




















})
