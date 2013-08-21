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

    ////////////////////////////////////////
    /// question animations

   $("#what button").click(function(event){
       event.preventDefault();
       //alert("click on next");
       $("#id option:selected").val();
       what = $("#what option:selected").val();
       $(".thingy").text(what.toLowerCase());
       //alert(what);
       $("#what").fadeOut();
       //$("#what").slideToggle();
       $("#how_much").removeClass("hidden");
       //$("#how_much").slideToggle();
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

   /////////////////////////////////

   $("#update a").click(function(event){
//      alert("update");
   $("#update_form").removeClass("hidden");
   });

    $("#update_form button").click(function(event){
       event.preventDefault();
       var frequency = parseInt($("#frequency").text());
       var mycost = parseFloat($("#cost").text());
       var update_frequency = $("#update_form input[name='update_frequency']")
       update_frequency = parseInt(update_frequency.val());
       var new_frequency = frequency + update_frequency;
       var new_cost_per_use = mycost / new_frequency;
       $("#frequency").text(new_frequency);
       $("#cost_per_use").text(new_cost_per_use);

       // recalculate the cost per use

       //send the info to the server.

       //do validations


       // alert(new_frequency);
    });
    // where the frequency lives
   //

});
