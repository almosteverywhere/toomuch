/**
 * Created with PyCharm.
 * User: julielavoie
 * Date: 2013-06-03
 * Time: 4:14 PM
 * To change this template use File | Settings | File Template**/


$(document).ready(function() {

   var what = "";
   var how_much = "";
   var how_many_times = "";

   $("#what button").click(function(event){
       event.preventDefault();
       //alert("click on next");
       $("#id option:selected").val();
       what = $("#what option:selected").val();
       $(".thingy").text(what);
       //alert(what);
       $("#what").fadeOut();
       $("#how_much").removeClass("hidden");

   });

    $("#how_much button").click(function(event){
       //alert("click on next");
       event.preventDefault();
       //todo, error handling here, what if no value
        how_much = $("#cost").val();
       //alert(how_much);
       $("#how_much").fadeOut();
       $("#how_many_times").removeClass("hidden");

   });

   $("#how_many_times button").click(function(event){
       event.preventDefault();
       //alert("click on next");
       //TODO error handling in case no value

       how_many_times = $("#how_often").val();
       $(".frequency").html(how_many_times);
       var cost_per_use = how_much;
       if (how_many_times !== 0) {
           cost_per_use = how_much / how_many_times;
       }
       cost_per_use = cost_per_use.toFixed(2) + "$";

       $("span#calculation").html(cost_per_use);

       $("#how_many_times").fadeOut();
       $("#result").removeClass("hidden");

   });

   $("#result a").click(function(){
       $("#result").fadeOut();
       $("#sign_up_form").removeClass("hidden");
       $("input[name='submit_thingy']").val(what);
       //ug my naming scheme is terrible
       $("input[name='submit_cost']").val(how_much);
       $("input[name='submit_frequency']").val(how_many_times);
   });

   $("#update a").click(function(event){
//      alert("update");
   $("#update_form").removeClass("hidden");
   });

   //if the user clicks sign up, we want to just show a sign in form




//    $("#add").click(function(){
//        var newRow = $("#template_row").clone().removeClass("hidden").attr("id", rowCounter).appendTo("#task_table");
//        //fixme: this could just bind the first one
//        newRow.find('.title').editable();
//
//        newRow.find('.number').editable();
//        newRow.find('.number').on('save', function(e, params) {
//
//            var mynum = parseInt(params.newValue);
//            var myHomeOfSquares = $(this).closest(".todo").find(".home_of_squares");
//            myHomeOfSquares.empty();
//            for (var i = 0; i < mynum; i++){
//                //fixme this needs to be the specific one
//                var squares = $(".square").first().clone().removeClass("hidden");
//                myHomeOfSquares.append('<div class="square"></div>');
//
//                console.log($(this).closest(".home_of_squares"), this);
//
//            }
//        });
//
//        newRow.find(".home_of_squares").on( 'click', '.square', function() {
//            $(this).toggleClass("completed");
//            $(this).prevAll().addClass("completed");
//        });
//
//        newRow.find('.quantity').editable();
//        newRow.find(".thingy").selectpicker();
//
//    });

});
